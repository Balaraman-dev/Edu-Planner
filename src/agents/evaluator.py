import json
from llm import call_llm
from utils.prompts import get_evaluator_prompt
from core.cidpp import compute_cidpp_score

class EvaluatorAgent:
    def __init__(self, model="meta-llama/llama-3.2-3b-instruct:free"):
        self.model = model

    def evaluate(self, lesson_plan: str, skill_tree) -> tuple[dict, dict]:
        skill_summary = skill_tree.get_summary()
        prompt = get_evaluator_prompt(lesson_plan, skill_summary)
        response = call_llm(prompt, temp=0.0, model=self.model)

        # Parse JSON response
        try:
            feedback = json.loads(response)
        except json.JSONDecodeError:
            # Fallback to old parsing if not JSON
            feedback = self._parse_legacy(response)

        score = compute_cidpp_score(feedback)
        return feedback, score

    def _parse_legacy(self, response: str) -> dict:
        scores = {}
        p_count = 0
        for line in response.split('\n'):
            line = line.strip()
            if not line or ']: ' not in line:
                continue
            try:
                start = line.find('[')
                end = line.find('] ')
                if start == -1 or end == -1:
                    continue
                tag = line[start+1:end]
                rest = line[end+1:].strip()
                if tag == 'P':
                    p_count += 1
                    key = 'Practicality' if p_count == 1 else 'Pertinence'
                else:
                    key_map = {'C': 'Clarity', 'I': 'Integrity', 'D': 'Depth'}
                    key = key_map.get(tag, tag)
                score_part = rest.split(';')[0].strip()
                score = int(score_part)
                scores[key] = {'score': score, 'strengths': [], 'weaknesses': [rest.split(';')[1].strip() if ';' in rest else '']}
            except:
                continue
        return scores
