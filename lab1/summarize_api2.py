import requests


def summarize_text2(text,num_sentences):
    
    url = "https://summarize-texts.p.rapidapi.com/pipeline"
    
    payload = { "input": text}
    
    headers = {
	"x-rapidapi-key": "9f3f445a19msh4f2d18d66be0e11p108007jsnce52789683e0",
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
