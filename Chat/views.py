from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .ai import get_ai_response, get_sentiment

# Create your views here.
@login_required
def chat_view(request):
    return render(request,"chat.html")

@login_required
def get_response(request):
    message=request.GET.get("message","").lower()
    reply=get_ai_response(message)

    return JsonResponse({"response": reply})

@login_required
def sentiment_response(request):
    message = request.GET.get("message","").lower()   
    reply = get_sentiment(message)
    return JsonResponse({"response": reply})