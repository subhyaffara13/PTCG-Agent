from typing import List

def cohere_message_pt(messages: list):
    tool_calls: List = get_all_tool_calls(messages=messages)
    prompt = ""
    tool_results = []
    for message in messages:
        # check if this is a tool_call result
        if message["role"] == "tool":
            tool_result = convert_openai_message_to_cohere_tool_result(
                message, tool_calls=tool_calls
            )
            tool_results.append(tool_result)
        elif message.get("content"):
            prompt += message["content"] + "\n\n"
    prompt = prompt.rstrip()
    return prompt, tool_results

