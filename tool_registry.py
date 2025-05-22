from tools import moodle_tools

tools = [
    {
        "name": "get_due_assignments",
        "description": "今日から指定された日数以内に〆切があるMoodle課題を取得する",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "今日から何日以内か"
                }
            },
            "required": ["days"]
        }
    },
    {
        "name": "check_new_messages",
        "description": "新着メッセージを取得する",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_pending_quizzes",
        "description": "まだ完了していない小テストを取得する（オプションで日数指定）",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "今日から何日以内に〆切のあるものか（省略可）"
                }
            }
        }
    },
    {
        "name": "get_my_courses",
        "description": "自分が所属しているMoodleのコース一覧を取得する",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

def get_tools():
    return tools

def call_tool(tool_name: str, arguments: dict):
    if tool_name == "get_due_assignments":
        return moodle_tools.get_due_assignments(**arguments)
    elif tool_name == "check_new_messages":
        return moodle_tools.check_new_messages(**arguments)
    elif tool_name == "get_pending_quizzes":
        return moodle_tools.get_pending_quizzes(**arguments)
    elif tool_name == "get_my_courses":
        return moodle_tools.get_my_courses()
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

