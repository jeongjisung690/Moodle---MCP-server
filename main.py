from fastapi import FastAPI
from moodle_api import get_assignments
from llm_ollama import generate_response

app = FastAPI()

@app.get("/ask")
def ask():
    print("/ask にリクエストを受信しました") 
    assignments = get_assignments()
    print(f"課題数: {len(assignments)}")
    reply = generate_response(assignments)
    print("応答生成完了")
    return {"response": reply}