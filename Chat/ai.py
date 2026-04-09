from transformers import pipeline
import os
from huggingface_hub import InferenceClient

chatbot = pipeline("text-generation", model="gpt2")

def get_ai_response(message):
    result = chatbot(message, max_length=100, num_return_sequences=1)
    return result[0]["generated_text"]



client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),
)

def get_sentiment(message):
    result = client.text_classification(
        message,
        model="tabularisai/multilingual-sentiment-analysis"
    )
    return str(result)