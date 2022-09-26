from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy


# Create your views here.

class Index(View):
    def get(self,request,*args,**kwargs):
        return render (request,'landing/index.html')
        # return render (request,'account/signup.html')


class Flash(View):
    def get(self,request,*args,**kwargs):
        return render (request,'landing/flash_page.html')
    
class Events(View):
    def get(self,request,*args,**kwargs):
        return render (request,'social/events.html')