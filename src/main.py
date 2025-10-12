from core.skill_tree import OSSkillTree
from agents.evaluator import EvaluatorAgent
from agents.optimizer import OptimizerAgent
from agents.analyst import AnalystAgent
from core.ciddp import compute_ciddp_score
import json

def main():

    # Step 1: Choose level
    print("Choose your level:")
    print("1. Easy\n2. Intermediate\n3. Hard")
    level_map = {"1": "easy", "2": "intermediate", "3": "hard"}
    level_choice = input("Enter 1, 2, or 3: ").strip()
    level = level_map.get(level_choice, "easy")

    # Step 2: Load questions
    questions_file = f"../data/os_questions_{level}.json"
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Step 3: Display MCQs and collect answers
    print(f"\nAnswer the following {level.capitalize()} OS questions:")
    user_answers = []
    for idx, q in enumerate(questions[:10], 1):
        print(f"\nQ{idx}: {q['question']}")
        # Generate MCQ options (correct + 3 random wrong answers)
        options = [q['answer']]
        # Collect wrong answers from other questions
        wrongs = [qq['answer'] for qq in questions if qq['answer'] != q['answer']]
        import random
        options += random.sample(wrongs, min(3, len(wrongs)))
        random.shuffle(options)
        for opt_idx, opt in enumerate(options, 1):
            print(f"  {opt_idx}. {opt}")
        ans = input("Your answer (1-4): ").strip()
        user_answers.append({
            "question": q['question'],
            "correct": q['answer'],
            "options": options,
            "user_choice": ans,
            "user_answer": options[int(ans)-1] if ans.isdigit() and 1 <= int(ans) <= len(options) else ""
        })

    # Step 4: Evaluate answers
    correct_count = sum(ua['user_answer'] == ua['correct'] for ua in user_answers)
    print(f"\nYou answered {correct_count} out of 10 questions correctly.")

    # Step 5: Prepare for further evaluation (lesson plan, skill tree, sample questions)
    skill_tree = OSSkillTree()
    skill_tree.set_level("Processes_and_Threads", 2)
    skill_tree.set_level("Memory_Management", 3)

    initial_plan = """
    Operating Systems Lesson Plan:
    1. Introduction to Operating Systems
    2. Processes and Threads
    3. Memory Management
    4. File Systems
    5. Device Management
    6. Scheduling and Multitasking
    7. Deadlocks and Synchronization
    8. Security and Protection
    9. Virtual Memory
    10. OS Architectures (Monolithic, Microkernel)
    """

    evaluator = EvaluatorAgent()
    optimizer = OptimizerAgent()
    analyst = AnalystAgent()

    best_plan = initial_plan
    best_score = 0
    score_queue = []
    best_plan_snapshot = initial_plan

    for iteration in range(3):
        print(f"\n--- Evaluator Agent (Iteration {iteration+1}) ---")
        try:
            scores, feedback = evaluator.evaluate(best_plan, skill_tree, sample_questions=user_answers)
        except ConnectionError as e:
            print(f"[Iter {iteration+1}] Ollama connection error: {e}")
            print("Skipping evaluation for this iteration.")
            continue

        avg_score = compute_ciddp_score(scores)
        score_queue.append({"score": avg_score, "scores": scores, "plan": best_plan})
        print(f"Evaluator CIDPP Score: {avg_score:.2f}")
        print(f"Evaluator Details: {scores}")

        # Find lagging area (lowest score)
        lag_area = min(scores, key=scores.get) if scores else None
        if lag_area:
            print(f"Lagging Area: {lag_area} (Score: {scores[lag_area]})")

        print("\n--- Optimizer Agent ---")
        if avg_score > best_score:
            best_score = avg_score
            best_plan_snapshot = best_plan
            best_plan = optimizer.optimize(best_plan, feedback, skill_tree)
            print("Lesson plan optimized based on feedback and lagging area.")

        print("\n--- Analyst Agent ---")
        error_notes = analyst.analyze_errors(best_plan, skill_tree)
        print("Common Pitfalls Suggested:")
        print(error_notes)
        best_plan += f"\n\nCommon Pitfalls:\n{error_notes}"

    # Show max CIDPP score and corresponding lesson plan
    max_score_entry = max(score_queue, key=lambda x: x["score"], default=None)
    if max_score_entry:
        print(f"\n Max CIDPP Score: {max_score_entry['score']:.2f}")
        print("\n==============================")
        print("🌟 Your Personalized OS Lesson Plan 🌟")
        print("==============================\n")
        # Split and format the lesson plan for clarity
        plan_lines = [line.strip() for line in max_score_entry["plan"].split('\n') if line.strip()]
        for line in plan_lines:
            if line.startswith("Common Pitfalls:"):
                print("\n🔎 " + line)
            elif line[0].isdigit() and line[1] == '.':
                print(f"  {line}")
            else:
                print(line)
        print("\n==============================")
        print("Ready to start your OS study journey! 🚀")
        print("==============================\n")
    else:
        print("No valid scores computed.")

if __name__ == "__main__":
    main()