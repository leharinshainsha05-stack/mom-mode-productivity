import datetime
import time
import json
import os
import matplotlib.pyplot as plt

def load_syllabus():
    if os.path.exists("syllabus.json"):
        # Added encoding="utf-8" to handle emojis
        with open("syllabus.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_syllabus(syllabus):
    # Added encoding="utf-8" to handle emojis
    with open("syllabus.json", "w", encoding="utf-8") as f:
        json.dump(syllabus, f, indent=4)

def mom_check():
    # 1. Your Jan 29 Deadline (Retained)
    deadline = datetime.datetime(2026, 1, 29, 9, 0, 0) 
    
    # Phase 2 Timeline
    sprint_start = datetime.datetime(2026, 2, 2, 0, 0, 0)
    master_goal_deadline = datetime.datetime(2026, 3, 22, 0, 0, 0)
    
    while True:
        now = datetime.datetime.now()
        syllabus = load_syllabus()
        
        time_left = deadline - now
        hours_left = int(time_left.total_seconds() // 3600)
        minutes_left = int((time_left.total_seconds() % 3600) // 60)

        print(f"\n" + "="*50)
        print(f"--- AGENTIC ASSISTANT: MOM MODE (Phase 2) ---")
        
        # 1. COLLEGE TRACKER
        if now < deadline:
            print(f"COLLEGE DEADLINE: {hours_left}h {minutes_left}m left! Keep going thambii!")
        else:
            print("COLLEGE: ALL MODULES DONE! 🎬 ENJOY THE MOVIE!")
        
        # 2. MISSION BRIEFING
        if now < sprint_start:
            sprint_diff = sprint_start - now
            s_days = sprint_diff.days
            s_hours = int(sprint_diff.total_seconds() // 3600) % 24
            s_mins = int(sprint_diff.total_seconds() // 60) % 60
            print(f"Mom Says: 'Get ready, thambii! UI/UX Sprint starts in {s_days}d {s_hours}h {s_mins}m!'")
        else:
            current_day_str = now.strftime("%a") 
            days_passed = (now - sprint_start).days
            target_week_idx = (days_passed // 7) + 1
            week_key = f"Week {target_week_idx}"
            
            if week_key in syllabus:
                lessons = syllabus[week_key].get("lessons", [])
                current_lesson = None
                for lesson in lessons:
                    if current_day_str.startswith(lesson["day"]):
                        current_lesson = lesson
                        break
                
                if current_lesson:
                    print("-" * 50)
                    print(f"🎯 GAME MISSION: {current_lesson['topic']}")
                    print(f"💌 {current_lesson['mission']}")
                else:
                    print(f"Mom Says: 'It's {now.strftime('%A')}, thambii. Catch up on your other tasks!'")
            else:
                if target_week_idx > 7:
                    print("Mom Says: 'Sprint completed! Proud of you!'")
                else:
                    print("Mom Says: 'Check your syllabus, thambii!'")
        
        # --- HIGH PRIORITY TRACKER ---
        print("-" * 50)
        high_priority_tasks = []
        try:
            with open("my_notebook.txt", "r") as file:
                for line in file:
                    if "| HIGH |" in line:
                        parts = line.split("|")
                        if len(parts) >= 4:
                            task_desc = parts[3].strip()
                            high_priority_tasks.append(task_desc)
        except FileNotFoundError:
            pass

        if high_priority_tasks:
            master_time_diff = master_goal_deadline - now
            days_until_master = int(master_time_diff.total_seconds() // 86400)
            print(f"Mom Says: 'Don't forget these URGENT tasks! You only have {days_until_master} days left for Phase 2!'")
            for task in high_priority_tasks:
                print(f"🔥 [URGENT] {task}")
        else:
            print("Mom Says: 'No high priority tasks! Good job, thambii.'")
        
        print("="*50)

        print("[A] Add Idea | [V] View All | [S] Search | [G] Goal Graph | [X] Delete | [D] Done | [Q] Quit")
        choice = input("Select an option: ").lower()

        if choice == 'a':
            new_thought = input("Enter idea: ")
            print("Priority: [1] High | [2] Medium | [3] Low")
            p_choice = input("Priority: ")
            priority = {"1": "HIGH", "2": "MEDIUM", "3": "LOW"}.get(p_choice, "LOW")
            category = input("Category: ").upper()
            
            if category == 'CALLS' or category == 'TALK':
                person = input("Mom Says: 'Who do you need to talk, thambii?': ")
                topic = input(f"Mom Says: 'And what is the topic for {person}?': ")
                new_thought = f"Person: {person} | Topic: {topic}"

            with open("my_notebook.txt", "a") as file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                file.write(f"[{timestamp}] | {priority} | {category} | {new_thought}\n")
            print("Mom Says: 'Noted! I've added it to your list.'")

        elif choice == 'v':
            print("\n--- YOUR NOTEBOOK ---")
            try:
                with open("my_notebook.txt", "r") as file:
                    for i, line in enumerate(file): print(f"[{i}] {line.strip()}")
            except FileNotFoundError: print("Notebook is empty!")

        elif choice == 'g':
            print("Mom Says: 'Click on a week bar to see your daily growth, thambii!'")
            syllabus = load_syllabus()
            
            weeks = [f"Week {i}" for i in range(1, 8)]
            week_display_titles = []
            colors = []

            for week in weeks:
                if week in syllabus:
                    full_title = syllabus[week].get("title", week)
                    clean_title = full_title.split(" (")[0] if " (" in full_title else full_title
                    week_display_titles.append(f"{week}: {clean_title}")
                    
                    lessons = syllabus[week].get("lessons", [])
                    done_count = sum(1 for l in lessons if l.get("status") == "completed")
                    colors.append('#4CAF50' if done_count == len(lessons) and len(lessons) > 0 else '#FFC107')
                else:
                    week_display_titles.append(week)
                    colors.append('#FFC107')

            fig, ax = plt.subplots(figsize=(10, 6))
            y_pos = list(range(len(week_display_titles)))
            display_titles = week_display_titles[::-1]
            
            ax.barh(y_pos, [100]*len(display_titles), color=colors[::-1])
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(display_titles)
            ax.set_title("UI/UX STRATEGIC ROADMAP (Click a week to drill down)")
            ax.set_xlabel("Progress (Green = Goal Reached, Yellow = In Progress)")

            def on_click(event):
                if event.inaxes == ax and event.ydata is not None:
                    try:
                        click_idx = int(round(event.ydata))
                        if 0 <= click_idx < len(weeks):
                            actual_week_num = len(weeks) - click_idx
                            selected_week = f"Week {actual_week_num}"
                            
                            if selected_week in syllabus:
                                plt.close(fig)
                                
                                lessons = syllabus[selected_week].get("lessons", [])
                                days = [l["day"] for l in lessons]
                                status_vals = [1 if l.get("status") == "completed" else 0 for l in lessons]
                                growth = [sum(status_vals[:i+1]) for i in range(len(status_vals))]

                                # NEW LOGIC: Only plot up to the last completed mission
                                completed_indices = [i for i, val in enumerate(status_vals) if val == 1]
                                # If nothing is done, show 0, otherwise show up to the latest done index
                                end_idx = max(completed_indices) + 1 if completed_indices else 1
                                
                                plt.figure(figsize=(10, 6))
                                # Plotting only the finished days to show 'growth'
                                plt.plot(days[:end_idx], growth[:end_idx], marker='o', linestyle='-', 
                                         color='#2196F3', linewidth=4, markersize=10)
                                plt.fill_between(days[:end_idx], growth[:end_idx], color='#2196F3', alpha=0.3)
                                
                                plt.title(f"🚀 YOUR GROWTH TREND: {selected_week}", fontsize=14, fontweight='bold')
                                plt.ylabel("Missions Completed", fontsize=12)
                                plt.xlabel("Days of the Week", fontsize=12)
                                plt.ylim(0, 7) # Fixed height for the 7 lessons
                                plt.xlim(0, 6) # Fixed width for the 7 days
                                plt.grid(True, linestyle='--', alpha=0.4)
                                plt.tight_layout()
                                plt.show()
                    except Exception as e:
                        print(f"Graph Error: {e}")

            fig.canvas.mpl_connect('button_press_event', on_click)
            plt.tight_layout()
            plt.show()

        elif choice == 'd':
            print("\n--- MARK TASK AS DONE ---")
            try:
                with open("my_notebook.txt", "r") as file:
                    lines = file.readlines()
                if not lines:
                    print("Your notebook is already empty, thambii!")
                else:
                    for i, line in enumerate(lines): print(f"[{i}] {line.strip()}")
                    idx = int(input("Enter the number [#] you finished: "))
                    done_line = lines.pop(idx)
                    parts = done_line.split("|")
                    if len(parts) >= 4:
                        task_desc = parts[3].strip()
                        for week_key, week_data in syllabus.items():
                            if isinstance(week_data, dict) and "lessons" in week_data:
                                for lesson in week_data.get("lessons", []):
                                    if lesson["topic"].lower() in task_desc.lower():
                                        lesson["status"] = "completed"
                                        save_syllabus(syllabus) 
                                        print(f"Mom Says: 'Smart Sync! I've marked {lesson['topic']} as completed!'")

                    with open("my_notebook.txt", "w") as file:
                        file.writelines(lines)
                    print(f"\nMom Says: 'Super! I've removed \"{done_line.strip()}\" from your list.'")
            except:
                print("Error: Could not find that task number!")

        elif choice == 'x': # Delete feature
            try:
                with open("my_notebook.txt", "r") as file:
                    lines = file.readlines()
                for i, line in enumerate(lines): print(f"[{i}] {line.strip()}")
                idx = int(input("Enter index [#] to delete: "))
                removed = lines.pop(idx)
                with open("my_notebook.txt", "w") as file:
                    file.writelines(lines)
                print(f"Mom Says: 'Deleted: {removed.strip()}'")
            except: print("Invalid index!")

        elif choice == 'q':
            break

if __name__ == "__main__":
    mom_check()