from django.urls import path
from .views import *

urlpatterns=[
    path('chat/',chat_view,name="chat"),
    path('chat/get-response/',get_response,name="get-response"),
    path('chat/get-sentiment/',sentiment_response,name="get-sentiment")
]