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
import re


# -------------------------------
# HELPER FUNCTION (DRY)
# -------------------------------
def save_chat(session, user, user_msg, bot_msg):
    ChatMessage.objects.create(
        user=user,
        session=session,
        role='user',
        content=user_msg
    )

    ChatMessage.objects.create(
        user=user,
        session=session,
        role='bot',
        content=bot_msg
    )


# -------------------------------
# HOME
# -------------------------------
def home(request):
    if request.user.is_authenticated:
              return render(request, "home.html")


# -------------------------------
# CHAT PAGE
# -------------------------------
@login_required
def chat_view(request, session_id=None):
    sessions = ChatSession.objects.filter(user=request.user).order_by('-id')

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
                title=""
            )
        return redirect('chat_session', session_id=current_session.id)

    # 🔥 Always ordered history
    history = ChatMessage.objects.filter(
        session=current_session
    ).order_by('timestamp')

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
        title=""
    )
    return redirect('chat_session', session_id=session.id)


# -------------------------------
# CHATBOT (MAIN CHAT)
# -------------------------------
@login_required
def get_response(request):
    try:
        message_text = request.GET.get("message", "").strip()
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
        if current_session.messages.count() == 1:
            clean_text = message_text.strip()
            clean_text = re.sub(r'[*#\-`]', '', clean_text)
            clean_text = re.sub(r'\s+', ' ', clean_text)

            words = clean_text.split()[:4]
            title = " ".join(words)

            current_session.title = title.capitalize()
            current_session.save()

        # Last 10 messages for context
        past_messages = ChatMessage.objects.filter(
            session=current_session
        ).order_by('-timestamp')[:40]

        past_messages = list(reversed(past_messages))

        messages = [
            {"role": "system", "content": "You are a smart, helpful AI assistant."}
        ]

        for msg in past_messages:
            role = "user" if msg.role == 'user' else "assistant"
            messages.append({
                "role": role,
                "content": msg.content
            })

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
        session_id = request.GET.get("session_id")

        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        result = get_sentiment(message)

        response_text = (
            f"{result['label']} ({result['score']})"
            if isinstance(result, dict)
            else str(result)
        )

        save_chat(current_session, request.user, message, response_text)

        return JsonResponse({"response": response_text})

    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# SUMMARY
# -------------------------------
@login_required
def summarize_response(request):
    try:
        message = request.GET.get("message", "")
        session_id = request.GET.get("session_id")

        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        result = get_summary(message)

        save_chat(current_session, request.user, message, result)

        return JsonResponse({"response": result})

    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# TRANSLATION
# -------------------------------
@login_required
def translation_response(request):
    try:
        message = request.GET.get("message", "")
        session_id = request.GET.get("session_id")

        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        result = get_translation(message)

        save_chat(current_session, request.user, message, result)

        return JsonResponse({"response": result})

    except Exception as e:
        return JsonResponse({"response": str(e)})


# -------------------------------
# GENERATION
# -------------------------------
@login_required
def generate_response(request):
    try:
        message = request.GET.get("message", "")
        session_id = request.GET.get("session_id")

        current_session = get_object_or_404(
            ChatSession,
            id=session_id,
            user=request.user
        )

        result = get_generation(message)

        save_chat(current_session, request.user, message, result)

        return JsonResponse({"response": result})

    except Exception as e:
        return JsonResponse({"response": str(e)})