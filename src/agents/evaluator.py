from llm import call_llm
from utils.prompts import get_evaluator_prompt

class EvaluatorAgent:
        def evaluate(self, lesson_plan: str, skill_tree, sample_questions=None) -> tuple[dict, str]:
            skill_summary = skill_tree.get_summary()
            prompt = get_evaluator_prompt(lesson_plan, skill_summary, sample_questions=sample_questions)
            response = call_llm(prompt, temp=0.0)

            scores = {}
            p_count = 0

            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    if not line.startswith('[') or ']' not in line:
                        continue

                    start = line.find('[')
                    end = line.find(']')
                    if start == -1 or end == -1 or end <= start:
                        continue

                    tag = line[start+1:end].strip()
                    rest = line[end+1:].strip()

                    if not rest.startswith(':'):
                        continue

                    # Extract score: everything after ':' until ';' or end
                    score_str = rest[1:].split(';')[0].strip()
                    score = int(score_str)

                    if tag == 'P':
                        p_count += 1
                        if p_count == 1:
                            key = 'Practicality'
                        elif p_count == 2:
                            key = 'Pertinence'
                        else:
                            key = f'P_{p_count}'
                    else:
                        key_map = {'C': 'Clarity', 'I': 'Integrity', 'D': 'Depth'}
                        key = key_map.get(tag, tag)

                    scores[key] = score
                    print(f" 9e1 {key}: {score}")

                except (ValueError, IndexError, AttributeError):
                    continue

            return scores, response