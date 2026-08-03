from typing import Optional

def _azure_tool_call_invoke_helper(
    function_call_params: ChatCompletionToolCallFunctionChunk,
) -> Optional[ChatCompletionToolCallFunctionChunk]:
    """
    Azure requires 'arguments' to be a string.
    """
    if function_call_params.get("arguments") is None:
        function_call_params["arguments"] = ""
    return function_call_params

