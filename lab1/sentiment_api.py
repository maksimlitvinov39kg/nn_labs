import requests

SENTIMENT_API_KEY = ''  

def analyze_sentiment_api(text):
    url = "https://sentiment-analisys.p.rapidapi.com/analyze-sentiment"
    
    payload = { "message": "{text}"}
    headers = {
        "x-rapidapi-key": "9f3f445a19msh4f2d18d66be0e11p108007jsnce52789683e0",
        "x-rapidapi-host": "sentiment-analisys.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return {
            'sentiment': result.get('sentiment', 'Нет информации'),
            'confidence': result.get('confidence', 0.0)
        }
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для анализа тональности: {e}")
        return None
