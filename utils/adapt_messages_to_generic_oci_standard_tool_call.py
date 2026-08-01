
def adapt_messages_to_generic_oci_standard_tool_call(
    role: str, tool_calls: list
) -> OCIMessage:
    """Convert an assistant tool-call message to OCI format."""
    tool_calls_formatted = []
    for tool_call in tool_calls:
        if not isinstance(tool_call, dict):
            raise OCIError(
                status_code=400, message="Each tool call must be a dictionary"
            )
        if tool_call.get("type") != "function":
            raise OCIError(
                status_code=400, message="OCI only supports function tool calls"
            )

        tool_call_id = tool_call.get("id")
        if not isinstance(tool_call_id, str):
            raise OCIError(status_code=400, message="Tool call `id` must be a string")

        tool_function = tool_call.get("function")
        if not isinstance(tool_function, dict):
            raise OCIError(
                status_code=400, message="Tool call `function` must be a dictionary"
            )

        function_name = tool_function.get("name")
        if not isinstance(function_name, str):
            raise OCIError(
                status_code=400, message="Tool call `function.name` must be a string"
            )

        arguments = tool_call["function"].get("arguments", "{}")
        if not isinstance(arguments, str):
            raise OCIError(
                status_code=400,
                message="Tool call `function.arguments` must be a JSON string",
            )

        tool_calls_formatted.append(
            OCIToolCall(
                id=tool_call_id,
                type="FUNCTION",
                name=function_name,
                arguments=arguments,
            )
        )

    return OCIMessage(
        role=open_ai_to_generic_oci_role_map[role],
        content=None,
        toolCalls=tool_calls_formatted,
        toolCallId=None,
    )

