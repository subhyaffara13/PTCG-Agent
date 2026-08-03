from typing import List, Optional, Union

def _should_convert_tool_call_to_json_mode(
    tool_calls: Optional[
        Union[List[ChatCompletionMessageToolCall], List[DatabricksTool]]
    ] = None,
    convert_tool_call_to_json_mode: Optional[bool] = None,
) -> bool:
    """
    Determine if tool calls should be converted to JSON mode
    """
    if (
        convert_tool_call_to_json_mode
        and tool_calls is not None
        and len(tool_calls) == 1
        and tool_calls[0]["function"]["name"] == RESPONSE_FORMAT_TOOL_NAME
    ):
        return True
    return False

