
def parse_messages(input):
    if input is None:
        return None

    def clean_message(message):
        # if is string, return as is
        if isinstance(message, str):
            return message

        if "message" in message:
            return clean_message(message["message"])

        serialized = {
            "role": message.get("role"),
            "content": message.get("content"),
        }

        # Only add tool_calls and function_call to res if they are set
        if message.get("tool_calls"):
            serialized["tool_calls"] = parse_tool_calls(message.get("tool_calls"))

        return serialized

    if isinstance(input, list):
        if len(input) == 1:
            return clean_message(input[0])
        else:
            return [clean_message(msg) for msg in input]
    else:
        return clean_message(input)

