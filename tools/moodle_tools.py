from datetime import datetime, timedelta, timezone
import requests
import json
import re

with open("config.json") as f:
    config = json.load(f)

MOODLE_URL = config["moodle"]["base_url"]
TOKEN = config["moodle"]["token"]

def get_my_userid():
    # 自分のユーザーIDを取得
    url = f"{MOODLE_URL}/webservice/rest/server.php"
    params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "core_webservice_get_site_info"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["userid"]

def unix_to_jst_str(unix_ts):
    # UTCのUNIXタイムスタンプをJST(UTC+9)に変換
    if not unix_ts:
        return ""

    dt_utc = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    dt_jst = dt_utc + timedelta(hours=9)
    return dt_jst.strftime("%Y-%m-%d %H:%M:%S JST")

def get_due_assignments(days: int):
    # 今日から指定された日数以内に〆切があるMoodle課題を取得する
    url = f"{MOODLE_URL}/webservice/rest/server.php"
    params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "mod_assign_get_assignments"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    now = datetime.now()
    deadline = now + timedelta(days=days)

    results = []
    for course in data.get("courses", []):
        for a in course.get("assignments", []):
            due = datetime.fromtimestamp(a["duedate"])
            if now <= due <= deadline:
                results.append({
                    "course": course["fullname"],
                    "name": a["name"],
                    "duedate": due.strftime("%Y-%m-%d")
                })
    return results

def html_to_text(html: str) -> str:
    """簡易的にHTMLタグを除去してテキスト化"""
    clean_text = re.sub(r'<[^>]+>', '', html)
    return clean_text.strip()

def check_new_messages(limit=10):
    # 新着メッセージを取得
    userid = get_my_userid()
    url = f"{MOODLE_URL}/webservice/rest/server.php"

    params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "core_message_get_conversations",
        "userid": userid,
        "limitfrom": 0,
        "limitnum": limit
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    conversations = data.get("conversations", [])
    results = []

    for conv in conversations:
        if conv.get("isread", True):
            continue  # 既読ならスキップ
        members = conv.get("members", [])
        messages = conv.get("messages", [])

        # 送信者名（自分以外の最初のメンバー名を想定）
        sender_name = "不明"
        if members:
            sender_name = members[0].get("fullname", "不明")

        for msg in messages:
            text_html = msg.get("text", "")
            text_plain = html_to_text(text_html)
            time_jst = unix_to_jst_str(msg.get("timecreated"))

            results.append({
                "from_name": sender_name,
                "text": text_plain,
                "timecreated": time_jst
            })

    return {
        "message_count": len(results),
        "messages": results
    }


def get_pending_quizzes(days: int = None):
    # 未完了の小テスト取得
    userid = get_my_userid()
    course_url = f"{MOODLE_URL}/webservice/rest/server.php"
    course_params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "core_enrol_get_users_courses",
        "userid": userid
    }

    course_response = requests.get(course_url, params=course_params)
    course_response.raise_for_status()
    courses = course_response.json()

    # course_ids = [course["id"] for course in courses]

    quiz_list = []

    for course in courses:
        course_id = course["id"]
        course_name = course["fullname"]

        # クイズ取得
        quiz_params = {
            "wstoken": TOKEN,
            "moodlewsrestformat": "json",
            "wsfunction": "mod_quiz_get_quizzes_by_courses",
            "courseids[0]": course_id
        }
        quiz_response = requests.get(course_url, params=quiz_params)
        quiz_response.raise_for_status()
        quizzes = quiz_response.json().get("quizzes", [])

        for quiz in quizzes:
            quiz_id = quiz["id"]
            timedue_ts = quiz.get("timedue")
            duedate = datetime.fromtimestamp(timedue_ts) if timedue_ts else None

            # days指定あり → 〆切でフィルター
            if days and duedate:
                now = datetime.now()
                deadline = now + timedelta(days=days)
                if not (now <= duedate <= deadline):
                    continue

            # 試行確認
            attempt_params = {
                "wstoken": TOKEN,
                "moodlewsrestformat": "json",
                "wsfunction": "mod_quiz_get_user_attempts",
                "quizid": quiz_id,
                "userid": userid
            }
            attempt_response = requests.get(course_url, params=attempt_params)
            attempt_response.raise_for_status()
            attempts = attempt_response.json().get("attempts", [])

            # 未完了のものだけ
            if not attempts or any(a["state"] in ["inprogress", "overdue"] for a in attempts):
                quiz_list.append({
                    "course": course_name,
                    "name": quiz["name"],
                    "duedate": duedate.strftime("%Y-%m-%d") if duedate else "期限なし"
                })
    


    return quiz_list

def get_my_courses():
    # 自分が所属しているコース一覧を取得
    userid = get_my_userid()
    url = f"{MOODLE_URL}/webservice/rest/server.php"
    params = {
        "wstoken": TOKEN,
        "moodlewsrestformat": "json",
        "wsfunction": "core_enrol_get_users_courses",
        "userid": userid
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    courses = response.json()

    return [
        {
            "id": c["id"],
            "shortname": c["shortname"],
            "fullname": c["fullname"]
        }
        for c in courses
    ]


