import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

MOODLE_URL = config["moodle"]["base_url"]
TOKEN = config["moodle"]["token"]

def get_assignments():
    endpoint = f"{MOODLE_URL}/webservice/rest/server.php"
    params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "mod_assign_get_assignments"
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    assignments = []
    for course in data.get("courses", []):
        for a in course.get("assignments", []):
            assignments.append({
                "course": course["fullname"],
                "name": a["name"],
                "duedate": a["duedate"]
            })
    return assignments
