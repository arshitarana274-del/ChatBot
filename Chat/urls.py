from django.urls import path
from .views import *

urlpatterns=[
    path('chat/',chat_view,name="chat"),
    path('chat/get-response/',get_response,name="get-response"),
    path('chat/get-sentiment/',sentiment_response,name="get-sentiment"),
    path('chat/get-summary/',summarize_response,name="get-summary"),
    path('chat/get-translation/',translation_response,name="get-translation"),
    path('chat/get-generation/',generate_response,name="get-generation") 
]