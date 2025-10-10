import json
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
    
    # Load questions
    with open("../data/os_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    # Filter by level, take up to 15
    filtered_questions = [q for q in questions if q["difficulty"].lower() == level][:15]
    
    print(f"\nAssessing your knowledge with {len(filtered_questions)} questions at {level.capitalize()} level.\n")
    
    scores = {}
    skill_tree = SkillTree(1,1,1,1,1)  # Start with beginner levels
    answers = []
    
    for i, q in enumerate(filtered_questions, 1):
        print(f"Q{i}: {q['example']}")
        user_answer = input("Your answer: ").strip()
        answers.append(user_answer)
    
    print("\nEvaluating answers...")
    
    for q, user_answer in zip(filtered_questions, answers):
        # Evaluate answer
        prompt = get_answer_evaluation_prompt(q['example'], user_answer)
        response = call_llm(prompt, temp=0.0)
        
        # Extract score (simple parsing)
        score = 3  # Default
        for line in response.splitlines():
            if "score" in line.lower():
                parts = line.lower().split("score")
                if len(parts) > 1:
                    digits = ''.join(filter(str.isdigit, parts[1]))
                    if digits:
                        score = int(digits)
                        break
            else:
                try:
                    score = int(line.strip())
                    break
                except:
                    continue
        
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
    initial_plan = f"Personalized Lesson for {level.capitalize()} on weak topics: {', '.join(weak_topics)}"
    
    evaluator = EvaluatorAgent(model="deepseek-r1")
    optimizer = OptimizerAgent(model="deepseek-r1")
    analyst = AnalystAgent(model="deepseek-r1")
    
    # Initial optimization loop
    for i in range(3):  # Initial 3 iterations
        feedback, score = evaluator.evaluate(initial_plan, skill_tree)
        initial_plan = optimizer.optimize(initial_plan, feedback, skill_tree)
        initial_plan = analyst.add_common_mistakes(initial_plan, skill_tree)
        if score["average"] >= 4.5:
            break
    
    print("\nInitial Optimized Lesson Plan:\n")
    print(initial_plan)
    
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
        
        # Test: 3 questions per topic
        test_scores = {}
        test_questions = topic_questions[:3]  # First 3
        for j, tq in enumerate(test_questions, 1):
            print(f"Test Q{j}: {tq['example']}")
            test_answer = input("Your answer: ").strip()
            
            prompt = get_answer_evaluation_prompt(tq['example'], test_answer)
            response = call_llm(prompt, temp=0.0)
            
            test_score = 3  # Default
            for line in response.splitlines():
                if "score" in line.lower():
                    parts = line.lower().split("score")
                    if len(parts) > 1:
                        digits = ''.join(filter(str.isdigit, parts[1]))
                        if digits:
                            test_score = int(digits)
                            break
                else:
                    try:
                        test_score = int(line.strip())
                        break
                    except:
                        continue
            
            test_scores[tq['example']] = test_score
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
