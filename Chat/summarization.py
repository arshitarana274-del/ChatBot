from transformers import pipeline

chatbot = pipeline("summarization", model="mT5_multilingual_XLSum")

def get_summarize_response(message):
    result = chatbot(message, max_length=150, min_length=30)
    return result[0]['summarize_text']