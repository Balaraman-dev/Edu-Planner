class AnalystAgent:
    def analyze_errors(self, example: str, skill_tree) -> str:
        prompt = f"""
Given this OS problem explanation:
"{example}"

Identify 3 common student misconceptions (e.g., confusing deadlock with starvation, thinking threads share stack, etc.) for students at this level:
{skill_tree.get_summary()}

Output as bullet points:
- Misconception 1: ...
- Misconception 2: ...
- Misconception 3: ...
"""
        return call_llm(prompt, temp=0.7)