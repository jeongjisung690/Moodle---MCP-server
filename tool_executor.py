from tools import moodle_tools

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
