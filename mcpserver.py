from flask import Flask, request, jsonify
import requests
import time
from config import MOODLE_API_URL, MOODLE_TOKEN

app = Flask(__name__)

@app.route("/mcp/query", methods=["POST"])
def mcp_query():
    data = request.get_json()
    query = data.get("query", "").lower()

    if "〆切" in query or "締切" in query:
        course_id = 233986  # ここを動的にすることも可能
        assignments = get_assignments(course_id)
        upcoming = filter_upcoming(assignments)
        return jsonify({"message": "締切が近い課題はこちらです", "assignments": upcoming})
    
    return jsonify({"message": "すみません、よく分かりませんでした。"})

def get_assignments(course_id):
    payload = {
        "wstoken": MOODLE_TOKEN,
        "wsfunction": "mod_assign_get_assignments",
        "moodlewsrestformat": "json",
        "courseids[0]": course_id
    }
    response = requests.post(MOODLE_API_URL, data=payload)
    data = response.json()
    
    assignments = []
    for course in data.get("courses", []):
        for assign in course.get("assignments", []):
            assignments.append({
                "name": assign["name"],
                "duedate": assign["duedate"]
            })
    return assignments

def filter_upcoming(assignments, within_hours=48):
    now = int(time.time())
    threshold = now + within_hours * 3600
    return [
        {
            "name": a["name"],
            "duedate": time.strftime('%Y-%m-%d %H:%M', time.localtime(a["duedate"]))
        }
        for a in assignments if now < a["duedate"] <= threshold
    ]

if __name__ == "__main__":
    app.run(debug=True)
