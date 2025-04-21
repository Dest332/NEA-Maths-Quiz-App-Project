import json
import os
from collections import defaultdict

def load_data(filename="users.json"):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            return {"users": {}}
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {"users": {}}

def save_data(data, filename="users.json"):
    # Save data to a file
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def calculate_score(correct_answers, total_questions):
    # Calculate the score as a percentage
    if total_questions <= 0:
        return 0
    if correct_answers < 0:
        correct_answers = 0
    score = (correct_answers / total_questions) * 100
    if score > 100:
        score = 100
    return int(score)

def calculate_average_score(user_data):
    # Calculate the average score for a user
    results = user_data.get("quiz_results", [])
    if len(results) == 0:
        return 0
    total = 0
    for result in results:
        total += result.get("score", 0)
    average = total / len(results)
    return round(average)

def get_student_scores(user_data):
    # Get highest scores for a student
    scores = defaultdict(dict)
    for result in user_data.get("quiz_results", []):
        topic = result["topic"]
        level = result["level"]
        score = result.get("score", 0)
        if level not in scores[topic] or score > scores[topic][level]:
            scores[topic][level] = score
    return scores

def load_student_data():
    # Load all student data
    data = load_data()
    if "users" not in data:
        print("Error: No users in data.")
        return []

    students = []
    for username, user_data in data["users"].items():
        if user_data.get("is_teacher", False) == False:
            if "quiz_results" not in user_data:
                print(f"Warning: No quiz results for {username}. Skipping.")
                continue
            scores = get_student_scores(user_data)
            students.append({
                "username": username,
                "scores": scores,
                "quiz_results": user_data.get("quiz_results", [])
            })
    return students

def update_student_results(username, quiz_data):
    # Update quiz results for a student
    data = load_data()
    if username not in data["users"]:
        data["users"][username] = {"quiz_results": []}
    user = data["users"][username]
    for level, score in quiz_data["level_scores"].items():
        user["quiz_results"].append({
            "topic": quiz_data["topic"],
            "level": f"Level {level}",
            "score": score
        })
    save_data(data)
    return True

def get_student_results(username):
    # Get results of a student
    data = load_data()
    if username in data["users"]:
        return data["users"][username].get("quiz_results", [])
    else:
        return []

def get_all_students_results():
    # Get results for all students
    data = load_data()
    students = []
    for username, user_data in data["users"].items():
        if user_data.get("is_teacher", False) == False:
            results = user_data.get("quiz_results", [])
            total_quizzes = len(results)
            avg_score = calculate_average_score(user_data)
            students.append({
                "username": username,
                "results": results,
                "total_quizzes": total_quizzes,
                "average_score": avg_score
            })
    return students