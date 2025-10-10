import json
from utils.prompts import get_analyst_prompt
from llm import call_llm

class AnalystAgent:
    def __init__(self, model="deepseek-r1"):
        self.model = model

    def add_common_mistakes(self, lesson_plan: str, skill_tree) -> str:
        skill_summary = skill_tree.get_summary()
        prompt = get_analyst_prompt(lesson_plan=lesson_plan, skill_summary=skill_summary)
        mistakes_section = call_llm(prompt, temp=0.7, model=self.model)
        return lesson_plan + "\n\n" + mistakes_section
