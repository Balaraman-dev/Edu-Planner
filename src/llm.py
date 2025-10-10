import ollama

def call_llm(prompt: str, model: str = "deepseek-r1", temp: float = 0.7) -> str:
    # Map model name if needed
    if model == "deepseek-r1":
        model = "qiangzhou7/deepseek-r1-8b-latest:latest"
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={"temperature": temp}
    )
    return response['response'].strip()
