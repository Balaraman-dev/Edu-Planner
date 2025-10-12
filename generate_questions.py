import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from src.llm import call_llm

def generate_mc_question(topic, knowledge, example, difficulty):
    prompt = f"""
You are an expert in Operating Systems. Based on the following information, create a multiple-choice question with 4 options (A, B, C, D), where one is correct.

Topic: {topic}
Knowledge: {knowledge}
Example Question: {example}
Difficulty: {difficulty}

Output ONLY a valid JSON object in this exact format:
{{
  "topic": "{topic}",
  "question": "The generated question text here",
  "options": {{
    "A": "Option A text",
    "B": "Option B text",
    "C": "Option C text",
    "D": "Option D text"
  }},
  "correct": "A",
  "difficulty": "{difficulty}"
}}

Ensure the question is clear, the correct answer is A, and options are plausible distractors.
"""
    response = call_llm(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for {topic}: {response}")
        return None

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(data_dir, "os_questions.json"), "r") as f:
        os_questions = json.load(f)

    beginner = []
    intermediate = []
    advanced = []

    for item in os_questions:
        topic = item["topic"]
        knowledge = item["knowledge"]
        example = item["example"]
        difficulty = item["difficulty"]

        num_questions = 5 if difficulty == "intermediate" else 1
        for _ in range(num_questions):
            mc_q = generate_mc_question(topic, knowledge, example, difficulty)
            if mc_q:
                if difficulty == "beginner":
                    beginner.append(mc_q)
                elif difficulty == "intermediate":
                    intermediate.append(mc_q)
                elif difficulty == "advanced":
                    advanced.append(mc_q)

    with open(os.path.join(data_dir, "beginner_questions.json"), "w") as f:
        json.dump(beginner, f, indent=2)

    with open(os.path.join(data_dir, "intermediate_questions.json"), "w") as f:
        json.dump(intermediate, f, indent=2)

    with open(os.path.join(data_dir, "advanced_questions.json"), "w") as f:
        json.dump(advanced, f, indent=2)

    print("Questions generated and saved.")

if __name__ == "__main__":
    main()
