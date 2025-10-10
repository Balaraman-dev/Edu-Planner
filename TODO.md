# TODO for EduPlanner OS Project Completion

## Completed Steps
- [x] Create `data/common_errors.json` with OS misconceptions.
- [x] Update `src/core/skill_tree.py`: Rename to SkillTree, update keys to match spec, add YAML loading.
- [x] Update `src/core/cidpp.py`: Rename file to cidpp.py, fix average computation, add JSON output support.
- [x] Update `src/agents/evaluator.py`: Add model init, JSON parsing for feedback with strengths/weaknesses, integrate CIDPP score.
- [x] Update `src/agents/optimizer.py`: Add model init, use self.model in LLM call.
- [x] Update `src/agents/analyst.py`: Rename method to add_common_mistakes, append section to plan, use self.model.
- [x] Update `src/utils/prompts.py`: Update for JSON output in evaluator, improve optimizer/analyst prompts.
- [x] Update `src/llm.py`: Map "deepseek-r1" to Ollama model, remove print.
- [x] Create `data/skill_tree_template.yaml` with default values.

## Pending Steps
- [ ] Update `src/main.py`: Restructure to spec's main loop (init SkillTree, fixed lesson_plan, loop with evaluate → optimize → add_mistakes until average >=4.5 or 5 iters, print final plan). Remove interactive question-answering.
- [ ] Test: Run `python src/main.py`, verify loop, CIDPP scores, misconceptions section, average >=4.5.
- [ ] Optional: Update requirements.txt if additional deps needed (e.g., deepseek if switching from Ollama).

## Next Steps
1. Edit main.py to implement the exact loop from task spec.
2. Execute `python src/main.py` to test.
3. If issues (e.g., LLM errors), debug via prompts or fallback.
