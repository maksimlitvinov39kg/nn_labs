import requests
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_sentiment_api(text):
    '''
    args:
    text -- текст, который необходимо проанализировать
    
    return:
    Результат анализа тональности текста в формате JSON или None в случае ошибки.
    '''
    url = "https://sentiment-analyzer3.p.rapidapi.com/Sentiment"
    
    querystring = {"text": text}
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "sentiment-analyzer3.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.text  
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для анализа тональности: {e}")
        return None
