from core.skill_tree import OSSkillTree
from agents.evaluator import EvaluatorAgent
from agents.optimizer import OptimizerAgent
from agents.analyst import AnalystAgent
from core.ciddp import compute_ciddp_score
import json

def main():
    # Initialize
    skill_tree = OSSkillTree()
    skill_tree.set_level("Processes_and_Threads", 2)
    skill_tree.set_level("Memory_Management", 3)

    # Initial lesson plan (could be LLM-generated or template)
    initial_plan = """
    Topic: Processes vs Threads
    Explanation: A process has its own memory space. Threads within a process share code, data, and heap but have private stacks.
    Example: In a web browser, one thread handles UI, another downloads files.
    """

    evaluator = EvaluatorAgent()
    optimizer = OptimizerAgent()
    analyst = AnalystAgent()

    best_plan = initial_plan
    best_score = 0

    for iteration in range(3):  # 3 optimization rounds
        scores, feedback = evaluator.evaluate(best_plan, skill_tree)
        avg_score = compute_ciddp_score(scores)
        print(f"[Iter {iteration+1}] CIDDP Score: {avg_score:.2f}")

        if avg_score > best_score:
            best_score = avg_score
            best_plan = optimizer.optimize(best_plan, feedback, skill_tree)

            # Analyze example part
            error_notes = analyst.analyze_errors(best_plan, skill_tree)
            best_plan += f"\n\nCommon Pitfalls:\n{error_notes}"

    print("\n✅ Final Optimized OS Lesson Plan:\n")
    print(best_plan)

if __name__ == "__main__":
    main()