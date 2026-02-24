import json
import os
from datetime import datetime

def load_syllabus():
    if os.path.exists("syllabus.json"):
        with open("syllabus.json", "r") as f:
            return json.load(f)
    return {}

def save_syllabus(syllabus):
    with open("syllabus_test.json", "w") as f:
        json.dump(syllabus, f, indent=4)

def test_fuzzy_match_and_save():
    print("\n--- Testing Fuzzy Match & Immediate Save ---")
    syllabus = load_syllabus()
    if not syllabus:
        print("❌ syllabus.json not found!")
        return

    # Reset a status for testing (Week 1, Lesson 1: Design Audits)
    syllabus["Week 1"]["lessons"][0]["status"] = "pending"
    
    task_desc = "Working on Design Audits for the project" # 'Design Audits' is the topic
    task_found = False
    
    # Logic extracted from goal_tracker.py [D] command
    for week_key, week_data in syllabus.items():
        if isinstance(week_data, dict) and "lessons" in week_data:
            for lesson in week_data.get("lessons", []):
                topic = lesson["topic"]
                if topic.lower() in task_desc.lower():
                    lesson["status"] = "completed"
                    save_syllabus(syllabus) # Immediate Save
                    task_found = True
                    print(f"Match found: {topic}")
    
    # Check if syllabus_test.json has 'completed'
    if os.path.exists("syllabus_test.json"):
        with open("syllabus_test.json", "r") as f:
            syllabus_check = json.load(f)
        
        status = syllabus_check["Week 1"]["lessons"][0]["status"]
        print(f"Final Status: {status}")
        if status == "completed":
            print("✅ Fuzzy Match & Save Success!")
        else:
            print("❌ Fuzzy Match & Save Failed!")
    else:
        print("❌ syllabus_test.json was not created!")

def test_graph_labels():
    print("\n--- Testing Graph Labels ---")
    syllabus = load_syllabus()
    if not syllabus:
        print("❌ syllabus.json not found!")
        return

    week_titles = []
    
    for i in range(1, 8):
        week_key = f"Week {i}"
        if week_key in syllabus:
            # Clean title logic from goal_tracker.py [G] command
            full_title = syllabus[week_key].get("title", f"Week {i}")
            title = full_title.split(" (")[0] if " (" in full_title else full_title
            week_titles.append(f"W{i}: {title}")
    
    print(f"Generated Titles: {week_titles}")
    expected_w1 = "W1: Quality Control"
    if week_titles and week_titles[0] == expected_w1:
        print("✅ Graph Labels Success!")
    else:
        print(f"❌ Graph Labels Failed! (Expected {expected_w1}, got {week_titles[0] if week_titles else 'None'})")

def test_mission_display():
    print("\n--- Testing Mission Display ---")
    # Simulate Monday, Feb 2nd 2026 (Sprint Start)
    now = datetime(2026, 2, 2, 10, 0, 0) 
    sprint_start = datetime(2026, 2, 2, 0, 0, 0)
    current_day_str = now.strftime("%a")
    
    days_passed = (now - sprint_start).days
    target_week_idx = (days_passed // 7) + 1
    week_key = f"Week {target_week_idx}"
    
    syllabus = load_syllabus()
    if not syllabus:
        print("❌ syllabus.json not found!")
        return

    if week_key in syllabus:
        lessons = syllabus[week_key].get("lessons", [])
        current_lesson = None
        for lesson in lessons:
            if current_day_str.startswith(lesson["day"]):
                current_lesson = lesson
                break
        
        if current_lesson:
            print(f"🎯 GAME MISSION: {current_lesson['topic']}")
            print(f"💌 {current_lesson['mission']}")
            if "Design Audits" in current_lesson['topic']:
                print("✅ Mission Display Success!")
            else:
                print("❌ Mission Display Failed!")
        else:
            print("❌ No lesson found for today!")
    else:
        print(f"❌ {week_key} not in syllabus!")

if __name__ == "__main__":
    test_fuzzy_match_and_save()
    test_graph_labels()
    test_mission_display()
    
    # Cleanup
    if os.path.exists("syllabus_test.json"):
        os.remove("syllabus_test.json")
