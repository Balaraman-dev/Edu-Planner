from llm import call_llm
from utils.prompts import get_evaluator_prompt

class EvaluatorAgent:
    def evaluate(self, lesson_plan: str, skill_tree) -> tuple[dict, str]:
        # Get skill summary from the skill_tree instance
        skill_summary = skill_tree.get_summary()
        prompt = get_evaluator_prompt(lesson_plan, skill_summary)
        response = call_llm(prompt, temp=0.0)

        scores = {}
        p_count = 0  # Track how many [P] entries we've seen

        for line in response.split('\n'):
            line = line.strip()
            if not line or ']: ' not in line:
                continue

            try:
                # Extract the tag inside [ ]
                start = line.find('[')
                end = line.find(']')
                if start == -1 or end == -1:
                    continue

                tag = line[start+1:end]  # e.g., 'C', 'I', 'D', 'P'
                rest = line[end+1:].strip()  # everything after ]

                # Handle the two P's
                if tag == 'P':
                    p_count += 1
                    if p_count == 1:
                        key = 'Practicality'
                    elif p_count == 2:
                        key = 'Pertinence'
                    else:
                        key = f'P_{p_count}'  # fallback
                else:
                    # Map single-letter tags to full names (optional but clearer)
                    key_map = {
                        'C': 'Clarity',
                        'I': 'Integrity',
                        'D': 'Depth'
                    }
                    key = key_map.get(tag, tag)

                # Extract score: first integer after ]: before ';'
                # Example: ":3; comment" → "3"
                score_part = rest.split(';')[0].strip()
                score = int(score_part)

                scores[key] = score
                print(f"  💕 {key}: {score}")

            except (ValueError, IndexError, AttributeError):
                # Skip lines that don't match expected format
                continue

        return scores, response