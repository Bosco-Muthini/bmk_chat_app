from django.urls import path 
from landing.views import Index, Flash, Events


urlpatterns=[
    path('',Index.as_view(),name='index'),
    path('flash', Flash.as_view(),name='flash_page'),
    path('events', Events.as_view(),name='events_page'),
]