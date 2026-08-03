import json
from typing import Optional

def _gemini_tool_call_invoke_helper(
    function_call_params: ChatCompletionToolCallFunctionChunk,
    tool_call_id: Optional[str] = None,
) -> Optional[VertexFunctionCall]:
    name = function_call_params.get("name", "") or ""
    arguments = function_call_params.get("arguments", "")
    if (
        isinstance(arguments, str) and len(arguments) == 0
    ):  # pass empty dict, if arguments is empty string - prevents call from failing
        arguments_dict = {
            "type": "object",
        }
    else:
        arguments_dict = json.loads(arguments)
    function_call = VertexFunctionCall(
        name=name,
        args=arguments_dict,
    )
    if tool_call_id:
        clean_id = tool_call_id.split(THOUGHT_SIGNATURE_SEPARATOR, 1)[0]
        if clean_id:
            function_call["id"] = clean_id
    return function_call

