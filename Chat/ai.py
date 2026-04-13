from huggingface_hub import InferenceClient
import os
from openai import OpenAI

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),
)

# -------------------------
chat_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# -------------------------
# CHAT
# -------------------------
def get_ai_response(messages):
    try:
        response = chat_client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------
# SENTIMENT
# -------------------------
def get_sentiment(message):
    try:
        result = client.text_classification(
            message,
            model="finiteautomata/bertweet-base-sentiment-analysis",
        )

        if not result:
            return {"label": "unknown", "score": 0}

        top = result[0]

        return {
            "label": top.get("label", "unknown"),
            "score": round(top.get("score", 0), 2)
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# SUMMARY
# -------------------------
def get_summary(message):
    try:
        result = client.summarization(
            message,
            model="facebook/bart-large-cnn"
        )
        return result.get("summary_text", "No summary generated.")

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------
# TRANSLATION
# -------------------------
def get_translation(message):
    try:
        response = chat_client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator. Translate English to Hindi accurately. Keep meaning correct, especially for stories and context."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------
# GENERATION 
# -------------------------
def get_generation(message):
    try:
        response = chat_client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": "Generate high-quality content."},
                {"role": "user", "content": message}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"