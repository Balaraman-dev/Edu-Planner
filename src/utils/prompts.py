"""
OS evaluation prompt templates (clean, error-free)
Provides three helper functions that return ready-to-use prompt strings for
an evaluator, an optimizer, and an analyst agent. Each function accepts the
lesson_plan and skill_summary and returns a formatted prompt that asks the
agent to evaluate using CIDDP criteria: Clarity, Integrity, Depth,
Practicality, Pertinence.
"""
from typing import Literal


def _format_scores_instructions() -> str:
    """Common output format instructions used by all prompts."""
    return (
        "Output ONLY a valid JSON object with keys 'Clarity', 'Integrity', 'Depth', 'Practicality', 'Pertinence'. "
        "Each value is a dict with 'score' (1-5 int), 'strengths' (list of str), 'weaknesses' (list of str). "
        "Example: {'Clarity': {'score': 3, 'strengths': ['Clear structure'], 'weaknesses': ['Too brief']}, ...}"
    )


def get_evaluator_prompt(lesson_plan: str, skill_summary: str) -> str:
    """Return a clean evaluator prompt for assessing an OS lesson plan.

    Args:
        lesson_plan: The full lesson plan text to evaluate.
        skill_summary: A one- to three-sentence summary of the student's
                       current skill level and prior knowledge.

    Returns:
        A formatted prompt string ready to feed to an evaluator LLM agent.
    """
    instructions = _format_scores_instructions()

    return (
        f"You are an expert Operating Systems instructor. Evaluate the following lesson plan using the 5D CIDPP framework.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Criteria:\n"
        f"- Clarity: Is the concept clearly explained?\n"
        f"- Integrity: Are all subtopics covered?\n"
        f"- Depth: Does it go beyond definitions (e.g., show scheduling algorithm comparisons)?\n"
        f"- Practicality: Are there real-world OS examples (e.g., Linux process scheduling)?\n"
        f"- Pertinence: Is it suited for the student’s skill-tree level?\n\n"
        f"{instructions}"
    )


def get_optimizer_prompt(lesson_plan: str, skill_summary: str, feedback: str = "") -> str:
    """Return a prompt guiding an optimizer agent to suggest concrete improvements."""
    feedback_section = f"Feedback to Address:\n{feedback}\n\n" if feedback.strip() else ""

    return (
        f"You are an expert curriculum optimizer for Operating Systems courses. Improve the lesson plan based on CIDPP feedback, targeting low-scoring dimensions.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"{feedback_section}"
        f"Original Lesson Plan:\n{lesson_plan}\n\n"
        f"Output: An optimized lesson plan that addresses weaknesses (e.g., add depth with comparisons, practicality with examples)."
    )


def get_analyst_prompt(lesson_plan: str, skill_summary: str) -> str:
    """Prompt to identify and append common OS misconceptions to a lesson plan."""
    return (
        f"You are an instructional analyst for Operating Systems. For the lesson plan below, identify 3 common misconceptions relevant to the topics, and provide clarifications.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Output: A markdown section '## Common Mistakes & Clarifications' with 3 bullets: '- Mistake: [error]\n  Clarification: [explanation]'.\n"
        f"Examples: Confusing process and thread differences; Believing deadlock = starvation; Thinking FIFO = Round Robin."
    )

# if _name_ == "_main_":
#     # quick sanity check example
#     example_lesson = "Intro to processes, context switching, simple round-robin scheduling."
#     example_skill = "Beginner: understands basic programming and threads, not OS internals."
#     print(get_evaluator_prompt(example_lesson, example_skill))


def get_answer_evaluation_prompt(question: str, user_answer: str) -> str:
    """Return a prompt to evaluate a user's answer to a question.

    Args:
        question: The question asked.
        user_answer: The user's answer text.

    Returns:
        A formatted prompt string for the LLM to evaluate the answer.
    """
    return (
        f"You are an expert Operating Systems instructor. Evaluate the following student answer for correctness and completeness.\n\n"
        f"Question: {question}\n"
        f"Student Answer: {user_answer}\n\n"
        f"Please provide a score from 1 to 5 and a brief explanation."
    )


def get_lesson_plan_generation_prompt(level: str, scores: dict) -> str:
    """Return a prompt to generate a personalized lesson plan based on scores.

    Args:
        level: The student's learning level.
        scores: A dictionary of question scores.

    Returns:
        A formatted prompt string for the LLM to generate a lesson plan.
    """
    scores_str = "\n".join([f"{k}: {v}" for k, v in scores.items()])
    return (
        f"You are an expert Operating Systems instructor. Generate a personalized lesson plan for a {level} student based on the following question scores:\n"
        f"{scores_str}\n\n"
        f"Create a lesson plan that addresses weak areas and reinforces strengths.\n"
        f"Include the key topics and contents the student must learn for each topic.\n"
        f"Also provide a summary of the CIDPP scores (Clarity, Integrity, Depth, Practicality, Pertinence) for the student's answers."
    )
