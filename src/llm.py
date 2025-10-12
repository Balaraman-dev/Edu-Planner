import requests

def call_llm(prompt: str, model: str = "meta-llama/llama-3.2-3b-instruct:free", temp: float = 0.7) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temp
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"OpenRouter API error: {response.status_code} {response.text}")
