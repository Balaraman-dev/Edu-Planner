from src.llm import call_llm

# Test the LLM call
try:
    response = call_llm("Hello, what is the capital of France?", model="deepseek/deepseek-r1", temp=0.0)
    print("LLM Response:", response)
    print("Test passed: LLM is working with OpenRouter API.")
except Exception as e:
    print("Test failed:", str(e))
