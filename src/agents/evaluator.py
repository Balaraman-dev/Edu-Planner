from llm import call_llm
from utils.prompts import get_evaluator_prompt

class EvaluatorAgent:
    def evaluate(self, lesson_plan: str, skill_tree) -> dict:
        prompt = get_evaluator_prompt(lesson_plan, skill_tree.get_summary())
        response = call_llm(prompt, temp=0.0)
        # Parse "[C]:4; ..." into dict
        scores = {}
        for line in response.split('\n'):
            if ']: ' in line:
                key = line.split(']')[0][1:]
                score = int(line.split(':')[1].split(';')[0])
                scores[key] = score
        return scores, response