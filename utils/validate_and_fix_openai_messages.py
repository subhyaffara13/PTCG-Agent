from typing import List

def validate_and_fix_openai_messages(messages: List):
    """
    Ensures all messages are valid OpenAI chat completion messages.

    Handles missing role for assistant messages.
    """
    new_messages = []
    for message in messages:
        if not message.get("role"):
            message["role"] = "assistant"
        if message.get("tool_calls"):
            message["tool_calls"] = jsonify_tools(tools=message["tool_calls"])

        convert_msg_to_dict = cast(AllMessageValues, convert_to_dict(message))
        cleaned_message = cleanup_none_field_in_message(message=convert_msg_to_dict)
        new_messages.append(cleaned_message)
    return validate_chat_completion_user_messages(messages=new_messages)

