from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .ai import (
    get_ai_response,
    get_sentiment,
    get_summary,
    get_translation,
    get_generation
)
from .models import ChatMessage, ChatSession


# -------------------------------
# CHAT PAGE
# -------------------------------
@login_required
def chat_view(request, session_id=None):
    sessions = ChatSession.objects.filter(user=request.user)

    if session_id:
        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )
    else:
        current_session = sessions.first()
        if not current_session:
            current_session = ChatSession.objects.create(
                user=request.user,
                title="First Chat"
            )
        return redirect('chat_session', session_id=current_session.id)

    history = current_session.messages.all()

    return render(request, "chat.html", {
        "history": history,
        "sessions": sessions,
        "current_session": current_session
    })


# -------------------------------
# NEW CHAT
# -------------------------------
@login_required
def new_chat(request):
    session = ChatSession.objects.create(
        user=request.user,
        title="New Chat"
    )
    return redirect('chat_session', session_id=session.id)


# -------------------------------
# CHATBOT (WITH MEMORY)
# -------------------------------
@login_required
def get_response(request):
    try:
        message_text = request.GET.get("message", "")
        session_id = request.GET.get("session_id")

        if not message_text or not session_id:
            return JsonResponse({"response": "Missing data."})

        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        # Save user message
        ChatMessage.objects.create(
            user=request.user,
            session=current_session,
            role='user',
            content=message_text
        )

        # Update title (first message)
        if current_session.messages.count() <= 2 and current_session.title == "New Chat":
            current_session.title = message_text[:30] + (
                '...' if len(message_text) > 30 else ''
            )
            current_session.save()

        # Fetch last 10 messages
        past_messages = current_session.messages.all().order_by('-timestamp')[:10]
        past_messages = reversed(past_messages)

        messages = [
            {
                "role": "system",
                "content": "You are a smart, helpful AI assistant."
            }
        ]

        for msg in past_messages:
            role = "user" if msg.role == 'user' else "assistant"
            messages.append({
                "role": role,
                "content": msg.content
            })

        # Get AI reply
        reply = get_ai_response(messages)

        if not reply:
            reply = "Sorry, I couldn't respond."

        # Save bot reply
        ChatMessage.objects.create(
            user=request.user,
            session=current_session,
            role='bot',
            content=reply
        )

        return JsonResponse({
            "response": reply,
            "title": current_session.title
        })

    except Exception as e:
        return JsonResponse({"response": f"Error: {str(e)}"})


# -------------------------------
# SENTIMENT
# -------------------------------
@login_required
def sentiment_response(request):
    try:
        message = request.GET.get("message", "")
        return JsonResponse({"response": get_sentiment(message)})
    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# SUMMARY
# -------------------------------
@login_required
def summarize_response(request):
    try:
        message = request.GET.get("message", "")
        return JsonResponse({"response": get_summary(message)})
    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# TRANSLATION
# -------------------------------
@login_required
def translation_response(request):
    try:
        message = request.GET.get("message", "")
        return JsonResponse({"response": get_translation(message)})
    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# GENERATION
# -------------------------------
@login_required
def generate_response(request):
    try:
        message = request.GET.get("message", "")
        return JsonResponse({"response": get_generation(message)})
    except Exception as e:
        return JsonResponse({"response": str(e)})