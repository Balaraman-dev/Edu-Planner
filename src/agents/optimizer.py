from utils.prompts import get_optimizer_prompt
from llm import call_llm

class OptimizerAgent:
    def __init__(self, model="meta-llama/llama-3.2-3b-instruct:free"):
        self.model = model


    def optimize(self, old_plan: str, feedback: str, skill_tree) -> str:
        skill_summary = skill_tree.get_summary()
        prompt = get_optimizer_prompt(
            lesson_plan=old_plan,
            skill_summary=skill_summary,
            feedback=str(feedback) 
        )
        return call_llm(prompt, temp=1.0, model=self.model)
