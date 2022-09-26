from django.shortcuts import render, redirect
from django.views import View
from social.models import Post, Comment, UserProfile, Notification, ThreadModel, MessageModel
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import PostForm, CommentForm, ShareForm, ThreadForm, MessageForm

# Create your views here.
#my own codes
class PostListView(LoginRequiredMixin, ListView):
    # model=Post
    # template_name='social/post_list.html'
    # def get(self, request,  *args, **kwargs):
        
    #     posts=Post.objects.all().order_by('-date_time')
    #     context={
    #         'post_list':posts,
    #     }
    #     return render(request, 'social/post_list.html', context)
    
    def get(self,request, *args, **kwargs):
        logged_in_user = request.user

        posts=Post.objects.all().order_by('-date_time')
        form = PostForm()
        share_form=ShareForm()

        context={
            'post_list':posts,
            'form':form,
            'shareform':share_form,
        }
        return render(request, 'social/post_list.html', context)
    def post(self,request, *args, **kwargs):
        posts=Post.objects.all().order_by('-date_time')
        form=PostForm(request.POST, request.FILES)
        share_form=ShareForm()
        # files = request.FILES.getlist('image')
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()

            # new_post.create_tags()

            # for f in files:
            #     img = Image(image=f)
            #     img.save()
            #     new_post.image.add(img)

            # new_post.save()

        context={
            'post_list':posts,
            'form':form,
            'shareform':share_form,
            
        }
        return render(request, 'social/post_list.html',context)

class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post=Post.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post=Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                date_time=original_post.date_time,
                shared_user=request.user,
                shared_on=timezone.now(),
                post_image=original_post.post_image,
            )

            new_post.save()  
        notification = Notification.objects.create(
            notification_type = 5,
            from_user = request.user,
            to_user = original_post.author,
            post = new_post,
        )

        return redirect('post_list')

class PostDetailView(View):
    def get(self,request, pk, *args, **kwargs):
        post=Post.objects.get(pk=pk)
        comment_form = CommentForm()
        comments=Comment.objects.filter(post=post).order_by('-date_time')
        context={
            'post':post,
            'form':comment_form,
            'comments':comments,
        }
        return render(request, 'social/post_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        post=Post.objects.get(pk=pk)
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.author=request.user 
            new_comment.post=post
            new_comment.save()

            # new_comment.create_tags()

        comments=Comment.objects.filter(post=post).order_by('-date_time')

        notification = Notification.objects.create(notification_type=2, from_user = request.user, to_user = post.author, post=post)

        context={
            'post':post,
            'form':comment_form,
            'comments':comments,
        }
        return render(request, 'social/post_detail.html',context)

class PostUploadView(CreateView):
    created_on=datetime.now().time()
    {'day':created_on}
    model=Post
    # form=PostForm
    # fields=['body']
    form_class=PostForm
    success_url=reverse_lazy('post_list')
    template_name='social/post_upload.html'
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=('body','choose_picture')
    template_name='social/post_edit.html'
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    template_name='social/post_delete.html'
    success_url=reverse_lazy('post_list')
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Comment
    template_name='social/comment_delete.html'
    # success_url=reverse_lazy('post_list')
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk':pk})
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 
class ProfileView(View):
    # model = UserProfile
    # template_name='social/profile.html'

    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-date_time')
        
        followers=profile.followers.all()
        if len(followers)==0:
            is_following=False

        for follower in followers:
            if follower == request.user:
                is_following=True
                break
            else:
                is_following=False

        number_of_followers=len(followers)
        context={
            'user':user,
            'profile':profile,
            'posts':posts,
            'number_of_followers':number_of_followers,
            'is_following':is_following,
        }
        return render(request, 'social/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=UserProfile
    fields=('name','bio','location','birth_date','education','work', 'place_of_work','skill','hobby','religion','status', 'profile_picture')
    template_name='social/profile_edit.html'
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('user_profile', kwargs={'pk':pk})
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3, from_user = request.user, to_user = profile.user)

        return redirect('user_profile', pk=profile.pk)
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect('user_profile', pk=profile.pk)
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post=Post.objects.get(pk=pk)
        
        is_dislike=False
        for dislike in post.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break

        if is_dislike:
            post.dislikes.remove(request.user)
        
        is_like=False
        
        for like in post.likes.all():
            if like==request.user:
                is_like=True
                break
        
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user = request.user, to_user = post.author, post=post)
        if is_like:
            post.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_like=False
        
        for like in post.likes.all():
            if like==request.user:
                is_like=True
                break
        
        if is_like:
            post.likes.remove(request.user)

        is_dislike=False
        
        for dislike in post.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment=Comment.objects.get(pk=pk)
        
        is_dislike=False
        for dislike in comment.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)
        
        is_like=False
        
        for like in comment.likes.all():
            if like==request.user:
                is_like=True
                break
        
        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user = request.user, to_user = comment.author, comment=comment)
        if is_like:
            comment.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        is_like=False
        
        for like in comment.likes.all():
            if like==request.user:
                is_like=True
                break
        
        if is_like:
            comment.likes.remove(request.user)

        is_dislike=False
        
        for dislike in comment.dislikes.all():
            if dislike==request.user:
                is_dislike=True
                break
        
        if not is_dislike:
            comment.dislikes.add(request.user)
        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment= Comment.objects.get(pk=pk)
        form=CommentForm(request.POST)

        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.author=request.user
            new_comment.post=post
            new_comment.parent=parent_comment
            new_comment.save()
        
        notification = Notification.objects.create(
            notification_type=2, 
            from_user = request.user, 
            to_user = parent_comment.author,
            comment=new_comment
            )

        return redirect('post_detail', pk=post_pk) 

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query=self.request.GET.get('query')
        profile_list=UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )
        post_list=Post.objects.filter(
            Q(author__username__icontains=query),
        )
        context={
            'profile_list':profile_list,
            'post_list':post_list,
        }
        return render(request, 'social/user_search.html', context)

class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        followers=profile.followers.all()
        context={
            'profile':profile,
            'followers':followers,
        }
        return render(request, 'social/followers_list.html', context)

class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen=True
        notification.save()

        return redirect('post_detail', pk=post_pk)

class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('user_profile', pk=profile_pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)

class SharedPostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        shared_post = Post.objects.get(pk=post_pk)
    # working but not displaying
        notification.user_has_seen=True
        notification.save()

        return redirect('post_detail', pk=post_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads':threads
        }

        return render(request, 'social/inbox.html', context)



class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
     
        context = {
            'form':form
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver=User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver,
                )
                thread.save()

                return redirect('thread', pk=thread.pk)

        except:
            messages.error(request, 'Invalid Username')
            return redirect('create_thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list=MessageModel.objects.filter(thread__pk__contains=pk)
        context={
            'thread':thread,
            'form':form,
            'message_list':message_list,
        }

        return render(request, 'social/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver=thread.user
        else:
            receiver=thread.receiver

        if form.is_valid():
            message=form.save(commit=False)
            message.thread=thread
            message.sender_user=request.user
            message.receiver_user=receiver
            message.save()

        # message = MessageModel(
        #     thread=thread,
        #     sender_user=request.user,
        #     receiver_user=receiver,
        #     body=request.POST.get('message'),
        # )

        # message.save()
        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread,
        )
        return redirect('thread', pk=pk)

class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=MessageModel
    template_name='social/message_delete.html'
    success_url=reverse_lazy('inbox')
    def test_func(self):
        message=self.get_object()
        return self.request.user == message.sender_user or message.receiver_user

class ThreadDeleteView( DeleteView):
    model=ThreadModel
    template_name='social/thread_delete.html'
    success_url=reverse_lazy('inbox')
    # def test_func(self):
    #     message=self.get_object()
    #     return self.request.user == threadmodel.user or threadmodel.receiver

class AccountDeleteView( DeleteView):
    model=UserProfile, ThreadModel, MessageModel, Comment, Post
    template_name='social/account_delete.html'
    success_url=reverse_lazy('account_logout')


#codessss
class PostView(LoginRequiredMixin, View):
    def get(self,request, *args, **kwargs):
        posts=Post.objects.all().order_by('-created_on')

        context={
            'post_list':posts,
        }
        return render(request, 'social/post.html', context)
    def post(self,request, *args, **kwargs):
        posts=Post.objects.all().order_by('-created_on')
        form=PostForm(request.POST)

        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=request.user
            new_post.save()
        context={
            'post_list':posts,
            'form':form,
        }
        return render(request, 'social/post.html',context)
class HisDetailView(LoginRequiredMixin, DetailView):
    def get(self,request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments=Comment.objects.filter(post=post).order_by('-date_time')
        context={
            'post':post,
            'form':form,
            'comments':comments,
        }
        return render(request, 'social/his_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        post=Post.objects.get(pk=pk)
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.author=request.user 
            new_comment.post=post
            new_comment.save()
        comments=Comment.objects.filter(post=post).order_by('-date_time')

        context={
            'post':post,
            'form':form,
            'comments':comments,
        }
        return render(request, 'social/his_detail.html',context)

class HisEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields=('body','choose_picture')
    template_name='social/his_edit.html'
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('his_detail', kwargs={'pk':pk})  
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 
class HisDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    template_name='social/his_delete.html'
    success_url=reverse_lazy('post_order')
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 
class HisCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Comment
    template_name='social/his_comment_delete.html'
    # success_url=reverse_lazy('post_order')
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('his_detail', kwargs={'pk':pk})
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author 







