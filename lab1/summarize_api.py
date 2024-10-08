import requests


def summarize_url_api(url):
    api_url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-url/"
    payload = {
        "url": url,
        "min_length": 100,
        "max_length": 300,
        "is_detailed": False
    }
    headers = {
        "x-rapidapi-key": "9f3f445a19msh4f2d18d66be0e11p108007jsnce52789683e0",
        "x-rapidapi-host": "tldrthis.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get('summary', 'Нет резюме')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API для суммаризации: {e}")
        return None
