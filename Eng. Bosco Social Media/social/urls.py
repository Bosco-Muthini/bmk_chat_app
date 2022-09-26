
from django.urls import path 
from social.views import(
 PostUploadView,
 PostListView,
 PostView,
 PostDetailView,
 HisDetailView,
 HisEditView,
 HisDeleteView,
 HisCommentDeleteView,
 PostDeleteView,
 PostUpdateView,
 CommentDeleteView,
 ProfileView,
 ProfileEditView,
 AddFollower,
 RemoveFollower,
 AddLike,
 AddDislike,
 UserSearch,
 ListFollowers,
 AddCommentLike,
 AddCommentDislike,
 CommentReplyView,
 PostNotification,
 ThreadNotification,
 FollowNotification,
 SharedPostNotification,
 RemoveNotification,
 SharedPostView,
 ListThreads,
 CreateThread,
 ThreadView,
 CreateMessage,
 MessageDeleteView,
 ThreadDeleteView,

 AccountDeleteView,

)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('post/upload',PostUploadView.as_view(), name='post_upload'),
    path('post/list',PostListView.as_view(), name='post_list'),
    path('post/<int:pk>',PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like', AddLike.as_view(), name='add_like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='add_dislike'),
    path('update/<int:pk>',PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name='post_delete'),
    path('post/<int:pk>/share',SharedPostView.as_view(),name='share_post'),

    path('notification/<int:notification_pk>/post/<int:post_pk>/', PostNotification.as_view(), name='post_notification'),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>/', FollowNotification.as_view(), name='follow_notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification_delete'),
    path('notification/<int:notification_pk>/thread/<int:object_pk>/', ThreadNotification.as_view(), name='thread_notification'),
    path('notification/<int:notification_pk>/shared_post/<int:post_pk>/', SharedPostNotification.as_view(), name='shared_post_notification'),

    path('post/<int:post_pk>/comment/<int:pk>/delete/', CommentDeleteView.as_view(),name='comment_delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment_like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment_dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment_reply'),

    path('profile/<int:pk>', ProfileView.as_view(),name='user_profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(),name='profile_edit'),
    path('profile/<int:pk>/followers', ListFollowers.as_view(), name='list_followers'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add_follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove_follower'),
    path('user/search', UserSearch.as_view(), name='profile_search'),
    path('account/delete/<int:pk>', AccountDeleteView.as_view(),name='account_delete'),

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create_thread/', CreateThread.as_view(), name='create_thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/compose/', CreateMessage.as_view(), name='create_message'),
    path('message/delete/<int:pk>',MessageDeleteView.as_view(),name='message_delete'),
    path('thread/delete/<int:pk>',ThreadDeleteView.as_view(),name='thread_delete'),

    path('post/order/',PostView.as_view(), name='post_order'),
    path('his/<int:pk>/',HisDetailView.as_view(), name='his_detail'),
    path('his/edit/<int:pk>/',HisEditView.as_view(),name='his_edit'),
    path('his/delete/<int:pk>/', HisDeleteView.as_view(), name='his_delete'),
    path('his/<int:post_pk>/hiscomment/delete/<int:pk>/',HisCommentDeleteView.as_view(), name='his_comment_delete'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

