from transformers import pipeline
from huggingface_hub import InferenceClient
import os

# Chat
chatbot = pipeline("text-generation", model="gpt2")
def get_ai_response(message):
    result = chatbot(message, max_length=100, num_return_sequences=1)
    return result[0]["generated_text"]


# Sentiment
client = InferenceClient(
    provider="hf-inference",
    api_key= os.getenv("HF_TOKEN"),
)
def get_sentiment(message):
    result = client.text_classification(
        message,
        model="tabularisai/multilingual-sentiment-analysis"
    )
    return str(result)

# Summarize
def get_summary(message):
    result = client.summarization(
        message,
        model="facebook/bart-large-cnn"
    )
    return result["summary_text"]

#translate
def get_translation(message):
    result=client.translation(
        message,
        model="Helsinki-NLP/opus-mt-en-hi"
    )
    return result["translation_text"]

#generate
def get_generation(message):
    result = chatbot(
        f"Generate high-quality content: {message}",
        max_length=150,
        num_return_sequences=1
    )
    return result[0]["generated_text"]