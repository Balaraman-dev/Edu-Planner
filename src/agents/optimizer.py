class OptimizerAgent:
    def optimize(self, lesson_plan: str, feedback: str, skill_tree) -> str:
        prompt = f"""
Improve the following OS lesson plan using this feedback:
{feedback}

Student Level: {skill_tree.get_summary()}

Keep it under 250 words. Focus on OS topics like process states, page tables, or deadlock.

Original:
{lesson_plan}

Revised Lesson Plan:
"""
        return call_llm(prompt, temp=1.0)