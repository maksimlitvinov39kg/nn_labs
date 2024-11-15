import requests
from dotenv import load_dotenv
import os

load_dotenv()

def summarize_text2(text, num_sentences):
    '''
    args:
    text -- текст, который необходимо суммировать
    num_sentences -- количество предложений в резюме
    
    return:
    Резюме текста в виде строки или 'Нет резюме' при отсутствии результата, 
    либо None в случае ошибки.
    '''
    url = "https://summarize-texts.p.rapidapi.com/pipeline"
    
    payload = { "input": text }
    
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"), 
        "x-rapidapi-host": "summarize-texts.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['output'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для суммаризации: {e}")
        return None  
