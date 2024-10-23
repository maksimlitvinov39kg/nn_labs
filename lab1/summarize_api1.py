import requests


def summarize_text1(text,num_sentences):
    url = "https://gpt-summarization.p.rapidapi.com/summarize"
    
    payload = { "text": text,
               "num_sentences": num_sentences}
    
    headers = {
	"x-rapidapi-key": "9f3f445a19msh4f2d18d66be0e11p108007jsnce52789683e0",
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
