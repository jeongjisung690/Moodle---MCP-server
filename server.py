import json
import openai
from tool_registry import get_tools, call_tool

with open("config.json") as f:
    config = json.load(f)

openai.api_key = config["llm"]["api_key"]


def handle_user_input(user_input: str):
    messages = [
        {"role": "system", "content": "あなたは大学のMoodleに詳しいアシスタントです。必要に応じてツールを使ってください。"},
        {"role": "user", "content": user_input}
    ]

    # ツール仕様を渡す（Function calling）
    response = openai.ChatCompletion.create(
        model=config["llm"]["model"],
        messages=messages,
        functions=get_tools(),
        function_call="auto"
    )

    choice = response.choices[0]
    if "function_call" in choice.message:
        func = choice.message["function_call"]
        name = func["name"]
        args = json.loads(func["arguments"])
        result = call_tool(name, args)

        # ツール結果を LLM に再送
        messages.append({
            "role": "assistant",
            "function_call": func
        })
        messages.append({
            "role": "function",
            "name": name,
            "content": json.dumps(result)
        })

        final_response = openai.ChatCompletion.create(
            model=config["llm"]["model"],
            messages=messages
        )
        return final_response.choices[0].message.content

    else:
        return choice.message.content
