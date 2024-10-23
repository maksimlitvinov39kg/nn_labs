import requests
from dotenv import load_dotenv
import os

load_dotenv()

def summarize_text1(text, num_sentences):
    '''
    args:
    text -- текст, который необходимо суммировать
    num_sentences -- количество предложений в резюме
    
    return:
    Резюме текста в виде строки или 'Нет резюме' при отсутствии результата, 
    либо None в случае ошибки.
    '''
    url = "https://gpt-summarization.p.rapidapi.com/summarize"
    
    payload = { 
        "text": text,
        "num_sentences": num_sentences
    }
    
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "gpt-summarization.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get('summary', 'Нет резюме') 
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для суммаризации: {e}")
        return None
