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
        "Output ONLY using these five short bracketed labels and a one-line comment for each:\n"
        "[C]:<score 1-5>; short comment  — Clarity\n"
        "[I]:<score 1-5>; short comment  — Integrity\n"
        "[D]:<score 1-5>; short comment  — Depth\n"
        "[P]:<score 1-5>; short comment  — Practicality\n"
        "[E]:<score 1-5>; short comment  — Pertinence\n"
        "Example output:\n"
        "[C]:3; Clear but too brief\n"
        "[I]:4; Good structure\n"
        "[D]:2; Lacks virtual memory details\n"
        "[P]:5; Uses real shell examples\n"
        "[E]:4; Matches beginner level"
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
        f"You are an expert Operating Systems instructor. Evaluate the following lesson plan using the CIDDP criteria (Clarity, Integrity, Depth, Practicality, Pertinence).\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Evaluate on:\n"
        f"- Clarity: Is the content simple, jargon-free, and easy to follow?\n"
        f"- Integrity: Does it cover necessary concepts and provide examples?\n"
        f"- Depth: Does it explain core OS topics (scheduling algorithms, paging, virtual memory, concurrency, etc.) with sufficient depth?\n"
        f"- Practicality: Are real OS examples (Linux/Windows commands, kernel behavior, shell examples) included and accurate?\n"
        f"- Pertinence: Is the lesson matched to the student's level and learning goals?\n\n"
        f"{instructions}"
    )


def get_optimizer_prompt(lesson_plan: str, skill_summary: str) -> str:
    """Return a prompt guiding an optimizer agent to suggest concrete improvements.

    The optimizer should propose edits, reorganizations, and add/outlines of missing examples or exercises.
    """
    instructions = _format_scores_instructions()

    return (
        f"You are an expert curriculum optimizer for Operating Systems courses. Using the CIDDP criteria, analyze the lesson plan below and produce concrete, prioritized improvement suggestions (short list).\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Tasks:\n"
        f"1) Provide 5 prioritized, actionable improvements (each 1--2 lines).\n"
        f"2) For each improvement, indicate which CIDDP area it affects (C/I/D/P/E).\n"
        f"3) Suggest one small in-lesson exercise or demo (1--3 steps) that addresses the top missing concept.\n\n"
        f"{instructions}"
    )


def get_analyst_prompt(lesson_plan: str, skill_summary: str, desired_outcome: str | None = None) -> str:
    """Return a prompt that asks an analyst agent to extract weaknesses and map them to remediation steps.

    Args:
        lesson_plan: Lesson plan text.
        skill_summary: Student skill profile.
        desired_outcome: Optional — the intended competence after the lesson (e.g., "be able to explain paging and implement a simple simulator").
    """
    instructions = _format_scores_instructions()
    outcome_line = f"Desired outcome: {desired_outcome}\n\n" if desired_outcome else ""

    return (
        f"You are an instructional analyst for Operating Systems. Read the lesson plan and identify gaps, misconceptions likely to arise, and remediation steps mapped to CIDDP criteria.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"{outcome_line}"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Tasks:\n"
        f"- List the top 5 weaknesses or likely misconceptions (one line each).\n"
        f"- For each weakness, provide a short remediation (1--2 sentences) and tag it with the affected CIDDP label(s).\n"
        f"- If applicable, include a single recommended resource or short in-class demo (title or 3-step outline).\n\n"
        f"{instructions}"
    )


# if _name_ == "_main_":
#     # quick sanity check example
#     example_lesson = "Intro to processes, context switching, simple round-robin scheduling."
#     example_skill = "Beginner: understands basic programming and threads, not OS internals."
#     print(get_evaluator_prompt(example_lesson, example_skill))