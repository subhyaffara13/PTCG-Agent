from typing import List, Optional, Tuple

def convert_tool_call_to_json_mode(
    tool_calls: List[ChatCompletionMessageToolCall],
    convert_tool_call_to_json_mode: bool,
) -> Tuple[Optional[Message], Optional[str]]:
    if _should_convert_tool_call_to_json_mode(
        tool_calls=tool_calls,
        convert_tool_call_to_json_mode=convert_tool_call_to_json_mode,
    ):
        # to support 'json_schema' logic on older models
        json_mode_content_str: Optional[str] = tool_calls[0]["function"].get(
            "arguments"
        )
        if json_mode_content_str is not None:
            message = litellm.Message(content=json_mode_content_str)
            finish_reason = "stop"
            return message, finish_reason
    return None, None

