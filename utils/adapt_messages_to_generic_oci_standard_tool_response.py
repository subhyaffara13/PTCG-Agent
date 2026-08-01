
def adapt_messages_to_generic_oci_standard_tool_response(
    role: str, tool_call_id: str, content: str
) -> OCIMessage:
    """Convert a tool-result message to OCI format."""
    return OCIMessage(
        role=open_ai_to_generic_oci_role_map[role],
        content=[OCITextContentPart(text=content)],
        toolCalls=None,
        toolCallId=tool_call_id,
    )

