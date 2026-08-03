from typing import Dict, List

def convert_openai_message_to_only_content_messages(
    messages: List[AllMessageValues],
) -> List[Dict[str, str]]:
    """
    Converts OpenAI messages to only content messages

    Used for calling guardrails integrations which expect string content
    """
    converted_messages = []
    user_roles = ["user", "tool", "function"]
    for message in messages:
        if message.get("role") in user_roles:
            converted_messages.append(
                {"role": "user", "content": convert_content_list_to_str(message)}
            )
        elif message.get("role") == "assistant":
            converted_messages.append(
                {"role": "assistant", "content": convert_content_list_to_str(message)}
            )
    return converted_messages

