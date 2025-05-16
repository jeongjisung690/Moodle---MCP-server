import requests
from datetime import datetime

def format_assignments(assignments):
    lines = []
    for a in sorted(assignments, key=lambda x: x['duedate']):
        due = datetime.fromtimestamp(a['duedate']).strftime('%Y-%m-%d')
        lines.append(f"- {a['course']} / {a['name']}：{due}")
    return "\n".join(lines)

def query_ollama(prompt, model='mistral'):
    print("Ollama に問い合わせ中…")  # デバッグ用ログ
    url = 'http://localhost:11434/api/chat'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Ollama からの応答あり")  # 応答確認ログ
    response.raise_for_status()
    return response.json()['message']['content']

def generate_response(assignments):
    assignment_text = format_assignments(assignments)
    prompt = (
        "ユーザが「〆切が近い課題を教えて」と言っています。\n"
        f"以下はそのユーザの課題リストです：\n{assignment_text}\n"
        "自然な日本語で返答してください。"
    )
    return query_ollama(prompt)
