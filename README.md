Agentic Assistant: Goal Tracker & UI/UX Roadmap

An automated, terminal-based productivity tool built in Python. This assistant acts as a "Mission Controller" for students, tracking deadlines, managing daily learning "missions," and visualizing progress through interactive roadmaps.

🚀 Key Features

Dynamic Countdown: Real-time tracking of the GSoC application deadline and Phase 2 sprint goals.

Mission Control Mode: Automatically pulls the daily learning topic and "mission" from a 7-week UI/UX syllabus based on the current date.

Smart Sync Notebook: A text-based logging system that allows users to add ideas with priority levels (High/Medium/Low).

Fuzzy Task Matching: When a task is marked as "Done," the assistant intelligently searches the JSON syllabus to auto-update progress.

Data Visualization: Uses Matplotlib to generate a "Strategic Roadmap." Features a drill-down capability: click on a week in the bar chart to see a detailed daily growth trend.

🛠️ Technical Implementation

1. Data Persistence

The system manages state across three different file types:

.json: Stores the complex, hierarchical UI/UX syllabus and completion statuses.

.txt: A lightweight, append-only log for quick ideas and urgent tasks.

.py: Logic handled via datetime for scheduling and matplotlib for the GUI.

2. The "Mom Mode" Logic

The assistant includes a "Mom Says" personality layer. It monitors the my_notebook.txt for any tasks marked with | HIGH | priority and generates urgent alerts if the Phase 2 deadline is approaching.

3. Verification Suite

Includes verify_fixes.py, a dedicated testing script that ensures:

Fuzzy matching logic correctly identifies topics.

JSON data saves correctly after modifications.

The visualization engine generates the correct labels for the UI/UX roadmap.

📦 Project Structure

goal_tracker.py: The main application loop and logic.

verify_fixes.py: Automated test suite for core functions.

syllabus.json: The 7-week curriculum data structure.

my_notebook.txt: Persistent storage for user thoughts and priority tasks.

🔧 How to Run

Ensure you have Python installed.

Install dependencies:

Bash
pip install matplotlib

Run the assistant:

Bash
python goal_tracker.py
