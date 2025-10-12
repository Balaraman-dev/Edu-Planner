import json
import os
import sys
sys.path.append(os.path.dirname(__file__))
from utils.prompts import get_answer_evaluation_prompt, get_lesson_plan_generation_prompt
from llm import call_llm
from core.skill_tree import SkillTree
from agents.evaluator import EvaluatorAgent
from agents.optimizer import OptimizerAgent
from agents.analyst import AnalystAgent
from core.cidpp import compute_cidpp_score

# Topic to skill dimension mapping
TOPIC_TO_DIM = {
    "Introduction_to_OS": "process_management",
    "Functions_of_OS": "process_management",
    "Types_of_OS": "process_management",
    "User_Interface": "process_management",
    "System_Calls": "process_management",
    "Kernel_vs_User_Mode": "process_management",
    "Processes": "process_management",
    "Threads": "process_management",
    "Process_Scheduling": "cpu_scheduling",
    "Synchronization_Basics": "synchronization_deadlocks",
    "Critical_Section_Problem": "synchronization_deadlocks",
    "Semaphores": "synchronization_deadlocks",
    "Deadlocks": "synchronization_deadlocks",
    "Deadlock_Avoidance": "synchronization_deadlocks",
    "Memory_Management": "memory_management",
    "Paging": "memory_management",
    "Segmentation": "memory_management",
    "Virtual_Memory": "memory_management",
    "Page_Replacement": "memory_management",
    "File_System": "file_systems",
    "I/O_Management": "file_systems",
    "Disk_Scheduling": "file_systems",
    "RAID": "file_systems",
    "System_Performance": "cpu_scheduling",
    "Security_and_Protection": "synchronization_deadlocks",
    "Distributed_Systems": "synchronization_deadlocks",
    "Real_Time_OS": "cpu_scheduling",
    "Virtualization": "memory_management",
    "Cloud_Computing_OS": "file_systems",
    "Modern_OS_Trends": "process_management"
}

def main():
    print("Welcome to the AI-powered OS Learning Assistant!")
    
    # Simple login
    username = input("Enter your username: ").strip()
    if not username:
        username = "Student"
    print(f"Welcome, {username}!")
    
    # Level selection
    level = ""
    while level.lower() not in ["beginner", "intermediate", "advanced"]:
        level = input("Choose your learning path (Beginner / Intermediate / Advanced): ").strip().lower()

    # Load detailed lesson plan
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "detailed_os_lesson_plan.md"), "r", encoding="utf-8") as f:
        detailed_lesson_plan = f.read()

    print(f"\nDetailed Operating Systems Lesson Plan:\n")
    print(detailed_lesson_plan)
    input("Press Enter to start the initial assessment...")

    # Load questions based on level
    if level == "beginner":
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "beginner_questions.json")
    elif level == "intermediate":
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "intermediate_questions.json")
    elif level == "advanced":
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "advanced_questions.json")
    else:
        raise ValueError("Invalid level selected")

    with open(file_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Take up to 15 questions
    filtered_questions = questions[:15]

    print(f"\nAssessing your knowledge with {len(filtered_questions)} questions at {level.capitalize()} level.\n")
    
    scores = {}
    skill_tree = SkillTree(1,1,1,1,1)  # Start with beginner levels
    answers = []
    
    for i, q in enumerate(filtered_questions, 1):
        print(f"Q{i}: {q['question']}")
        for opt in q['options']:
            print(f"{opt}: {q['options'][opt]}")
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        answers.append(user_answer)
    
    print("\nEvaluating answers...")
    
    for q, user_answer in zip(filtered_questions, answers):
        # Check if answer is correct
        correct = user_answer == q['correct']
        score = 5 if correct else 1  # 5 for correct, 1 for incorrect

        topic = q['topic']
        scores[topic] = score
        print(f"Score for {topic}: {score}/5")

        # Update skill tree
        dim = TOPIC_TO_DIM.get(topic, "process_management")  # Default
        skill_level = min(5, max(1, score))  # Map 1-5 directly
        skill_tree.set_level(dim, skill_level)
    
    print("Assessment complete. Initializing personalized learning...")
    
    # Generate initial lesson plan based on weak areas
    weak_topics = [t for t, s in scores.items() if s < 3]
    if weak_topics:
        analysis = f"Analysis: The student has weak areas in the following topics: {', '.join(weak_topics)}. The lesson plan will focus on these to improve understanding."
        initial_plan = f"{analysis}\n\nPersonalized Lesson for {level.capitalize()} on weak topics: {', '.join(weak_topics)}"
    else:
        analysis = "Analysis: The student has demonstrated strong knowledge in all assessed topics, scoring perfectly. Therefore, a comprehensive beginner lesson plan is provided to reinforce and deepen understanding of all fundamental OS concepts."
        lesson_content = """
Comprehensive Beginner Lesson Plan for Operating Systems

**Objective:** Introduce fundamental concepts of Operating Systems to beginners.

**Topics to Cover:**

1. **Introduction to OS**
   - What is an Operating System?
   - Role and importance in computing.

2. **Functions of OS**
   - Process management, memory management, file handling, device control.

3. **Types of OS**
   - Batch, interactive, real-time, distributed, etc.

4. **User Interface**
   - CLI vs GUI.

5. **System Calls**
   - How applications interact with OS.

6. **Kernel vs User Mode**
   - Protection and privilege levels.

7. **Processes**
   - Definition, states, process control block.

8. **Threads**
   - Multithreading, benefits over processes.

9. **Process Scheduling**
   - Algorithms: FCFS, SJF, Round Robin.

10. **Synchronization Basics**
    - Race conditions, critical sections.

11. **Semaphores and Deadlocks**
    - Synchronization tools, deadlock prevention.

12. **Memory Management**
    - Allocation, paging, segmentation, virtual memory.

13. **File Systems**
    - Organization, directories, permissions.

14. **I/O Management**
    - Device drivers, scheduling.

15. **Other Topics**
    - Security, distributed systems, modern trends.

**Learning Activities:** Explanations, examples, quizzes.
"""
        initial_plan = f"{analysis}\n\n{lesson_content}"
    
    evaluator = EvaluatorAgent(model="deepseek/deepseek-r1")
    optimizer = OptimizerAgent(model="deepseek/deepseek-r1")
    analyst = AnalystAgent(model="deepseek/deepseek-r1")
    
    # Initial optimization loop
    for i in range(3):  # Initial 3 iterations
        feedback, score = evaluator.evaluate(initial_plan, skill_tree)
        initial_plan = optimizer.optimize(initial_plan, feedback, skill_tree)
        initial_plan = analyst.add_common_mistakes(initial_plan, skill_tree)
        if score["average"] >= 4.5:
            break
    
    print("\nInitial Optimized Lesson Plan:\n")
    print(initial_plan)

    # Test after lesson plan: 10 questions
    print("\nNow, let's test your understanding with 10 questions based on the lesson plan.")
    input("Press Enter when ready for the test...")

    test_scores = {}
    test_questions = filtered_questions[:10]  # First 10 questions
    for j, tq in enumerate(test_questions, 1):
        print(f"Test Q{j}: {tq['question']}")
        for opt in tq['options']:
            print(f"{opt}: {tq['options'][opt]}")
        test_answer = input("Your answer (A/B/C/D): ").strip().upper()

        # Check if answer is correct
        correct = test_answer == tq['correct']
        test_score = 5 if correct else 1  # 5 for correct, 1 for incorrect

        test_scores[tq['question']] = test_score
        print(f"Test Score: {test_score}/5\n")

    # Update skill tree based on test
    avg_test_score = sum(test_scores.values()) / len(test_scores)
    print(f"Average Test Score: {avg_test_score}/5")

    # Group questions by topic for per-topic learning
    topic_groups = {}
    for q in filtered_questions:
        topic = q['topic']
        if topic not in topic_groups:
            topic_groups[topic] = []
        topic_groups[topic].append(q)
    
    for topic, topic_questions in topic_groups.items():
        print(f"\n--- Learning Topic: {topic} ---")
        print("Lesson Plan for this topic:\n")
        topic_plan = initial_plan.replace("weak topics", topic)  # Simple adaptation
        print(topic_plan)
        
        input("Press Enter when ready for the test...")
        
        # Test: 10 questions per topic
        test_scores = {}
        test_questions = topic_questions[:10]  # First 10
        for j, tq in enumerate(test_questions, 1):
            print(f"Test Q{j}: {tq['question']}")
            for opt in tq['options']:
                print(f"{opt}: {tq['options'][opt]}")
            test_answer = input("Your answer (A/B/C/D): ").strip().upper()

            # Check if answer is correct
            correct = test_answer == tq['correct']
            test_score = 5 if correct else 1  # 5 for correct, 1 for incorrect

            test_scores[tq['question']] = test_score
            print(f"Test Score: {test_score}/5\n")
        
        # Re-update skill tree based on test
        dim = TOPIC_TO_DIM.get(topic, "process_management")
        avg_test_score = sum(test_scores.values()) / len(test_scores)
        skill_level = min(5, max(1, round(avg_test_score)))
        skill_tree.set_level(dim, skill_level)
        
        # Re-optimize lesson plan
        print("Re-optimizing lesson plan based on test results...")
        for k in range(2):  # 2 iterations per topic
            feedback, score = evaluator.evaluate(topic_plan, skill_tree)
            topic_plan = optimizer.optimize(topic_plan, feedback, skill_tree)
            topic_plan = analyst.add_common_mistakes(topic_plan, skill_tree)
            if score["average"] >= 4.5:
                break
        
        print(f"Updated Lesson Plan for {topic}:\n")
        print(topic_plan)
    
    print("\nLearning session complete! Your skill tree summary:")
    print(skill_tree.get_summary())

if __name__ == "__main__":
    main()
