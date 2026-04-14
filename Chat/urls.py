from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name="chat"),
    path('chat/<int:session_id>/', views.chat_view, name="chat_session"),
    path('chat/new/', views.new_chat, name="new_chat"),
    path('chat/get-response/', views.get_response, name="get-response"),
    path('chat/get-sentiment/', views.sentiment_response, name="get-sentiment"),
    path('chat/get-summary/', views.summarize_response, name="get-summary"),
    path('chat/get-translation/', views.translation_response, name="get-translation"),
    path('chat/get-generation/', views.generate_response, name="get-generation"),
]