
def function_call_prompt(messages: list, functions: list):
    function_prompt = """Produce JSON OUTPUT ONLY! Adhere to this format {"name": "function_name", "arguments":{"argument_name": "argument_value"}} The following functions are available to you:"""
    for function in functions:
        function_prompt += f"""\n{function}\n"""

    function_added_to_prompt = False
    for message in messages:
        if "system" in message["role"]:
            if isinstance(message["content"], str):
                message["content"] += f""" {function_prompt}"""
            else:
                message["content"].append(
                    {"type": "text", "text": f""" {function_prompt}"""}
                )
            function_added_to_prompt = True

    if function_added_to_prompt is False:
        messages.append({"role": "system", "content": f"""{function_prompt}"""})

    return messages

