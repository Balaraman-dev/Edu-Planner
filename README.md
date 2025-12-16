🎓 EDU PLANNER — LLM-Based Multi-Agent System for Automated Lesson Plan Generation

EduPlanner is an intelligent, multi-agent system designed to automate, refine, and personalize academic lesson planning. It transforms traditional manual planning into a scalable, adaptive, curriculum-aligned workflow powered by LLMs and automated evaluators.

This project was built as a major academic project, focused on solving the major inefficiencies in conventional lesson planning.

🚨 Problem Space — Why EduPlanner?

Traditional lesson planning is often:
1️⃣ Time-Consuming — Teachers spend hours creating structured plans.

2️⃣ Not Personalized — Plans rarely adapt to student progress/levels.

3️⃣ No Iterative Optimization — Once created, they are not refined.

4️⃣ Standardized & Rigid — No dynamic evaluation system.

5️⃣ Manual & Dependent — High effort with limited automation.


EduPlanner solves these with an automated multi-agent pipeline.

🧠 Core Multi-Agent Architecture
✔ 1. Evaluator Agent — CIDPP Framework

Evaluates the generated lesson plan across five dimensions:

Clarity

Instructional Depth

Difficulty Progression

Personalization

Pedagogical Structure

✔ 2. Optimizer Agent

Iteratively refines the lesson plan to improve structure, quality, and curriculum alignment. Think of it as a “lesson plan fine-tuner.”

✔ 3. Analyst Agent

Detects errors, flags inconsistencies, and enhances reliability with automated warnings and corrections.

🔧 Technical Contributions & Implementations

✔ Multi-Subject Curriculum Expansion
✔ Migration to Open-Weight LLMs (Local + Cloud)
✔ Versioned Lesson Plan System
✔ Personalization Layer Based on Student Progress
✔ Teacher-Centric Web Interface (React)

🔮 Future Enhancements

📄 Automated report generation

🧑‍🏫 Teacher collaboration + editing tools

📚 LMS / EdTech integration

🎨 Multimodal (text + images) lesson generation

🗣 Voice input + multilingual support

⚠️ Project Challenges

💰 High inference cost of large LLMs

💻 Hardware limitations (recommended ≥ 8GB RAM)

🎯 Subjective nature of LLM-based evaluation

🚫 No teacher approval loop yet

🐌 Slow iterative optimization due to model latency

📥 Installation Guide (Detailed & Step-by-Step)

Follow these steps to set up EduPlanner on your local system.

🖥️ 1. Prerequisites

Make sure you have the following installed:

✔ Node.js (v18+)

Download: https://nodejs.org

✔ npm or yarn

Comes with Node.js

✔ Python 3.10+ (if running local LLM backend)
✔ Git

Download: https://git-scm.com

✔ (Optional) Local LLM Runtime

If using open-weight models locally:

Ollama

LM Studio

HuggingFace Text-Generation-Inference
(Choose depending on your system capabilities)

📦 2. Clone the Repository
git clone https://github.com/Balaraman-dev/Edu-Planner.git
cd Edu-Planner

📂 3. Install Dependencies
Install backend dependencies (if there is a backend folder):
cd backend
pip install -r requirements.txt


OR if using Node backend:

cd backend
npm install

Install frontend dependencies:
cd ../frontend
npm install

🔑 4. Configure Environment Variables

Create a .env file in both frontend & backend folders.

Examples:

Backend .env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini


OR for local LLM:

LOCAL_LLM_URL=http://localhost:11434/api/generate
MODEL_NAME=llama3

Frontend .env
VITE_API_URL=http://localhost:5000

▶️ 5. Running the Application
⚙️ Start the Backend

For Python backend:

cd backend
python app.py


For Node backend:

cd backend
npm run dev


Backend will start on:

👉 http://localhost:5000

🌐 Start the Frontend
cd frontend
npm run dev


Frontend will start on:

👉 http://localhost:5173

🧪 6. Using EduPlanner — Full Workflow

Once both servers are running:

🏁 Step 1 — Enter subject & academic standard

Eg: Mathematics, Grade 8

🧩 Step 2 — Multi-Agent Workflow Begins

Generator → Creates initial draft

Evaluator Agent → Scores the plan

Optimizer Agent → Refines based on score

Analyst Agent → Flags errors & finalizes

📝 Step 3 — View Final Lesson Plan

Download

Save Version

Regenerate / optimize again

📚 Step 4 — Track Version History

Each refinement creates a versioned plan for teachers.

👥 Step 5 — Personalization Layer

If student progress data is provided → EduPlanner adapts lesson difficulty.

🗄️ 7. Folder Structure (Clean & Professional)
Edu-Planner/
│── backend/
│   ├── models/
│   ├── agents/
│   ├── routes/
│   ├── utils/
│   └── app.py / server.js
│
│── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── App.jsx
│
└── README.md
![login](https://github.com/user-attachments/assets/ea22cbfa-8668-46e8-afb4-ae21f2ba2f7d)![lp]

(https://github.com/user-attachments/assets/9faa9316-f813-45dd-9663-a8fea8733dec)

![path](https://github.com/user-attachments/assets/73de2b6c-71b2-48da-bb0b-ed27681de8f4)

![Uploading lessonplan.jpg…]()



