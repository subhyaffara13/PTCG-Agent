from typing import Any, Dict, List

def handle_any_messages_to_chat_completion_str_messages_conversion(
    messages: Any,
) -> List[Dict[str, str]]:
    """
    Handles any messages to chat completion str messages conversion

    Relevant Issue: https://github.com/BerriAI/litellm/issues/9494
    """
    import json

    if isinstance(messages, list):
        try:
            return cast(
                List[Dict[str, str]],
                handle_messages_with_content_list_to_str_conversion(messages),
            )
        except Exception:
            return [{"input": json.dumps(message, default=str)} for message in messages]
    elif isinstance(messages, dict):
        try:
            return [{"input": json.dumps(messages, default=str)}]
        except Exception:
            return [{"input": str(messages)}]
    elif isinstance(messages, str):
        return [{"input": messages}]
    else:
        return [{"input": str(messages)}]

