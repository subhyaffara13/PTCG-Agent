from typing import List

def adapt_messages_to_generic_oci_standard(
    messages: List[AllMessageValues],
) -> List[OCIMessage]:
    """Convert an OpenAI-format message array to OCI GENERIC format."""
    new_messages = []
    for message in messages:
        role = message["role"]
        content = message.get("content")
        tool_calls = message.get("tool_calls")
        tool_call_id = message.get("tool_call_id")

        if role == "assistant" and tool_calls is not None:
            if not isinstance(tool_calls, list):
                raise OCIError(
                    status_code=400, message="Message `tool_calls` must be a list"
                )
            new_messages.append(
                adapt_messages_to_generic_oci_standard_tool_call(role, tool_calls)
            )

        elif role in ["system", "user", "assistant"] and content is not None:
            if not isinstance(content, (str, list)):
                raise OCIError(
                    status_code=400,
                    message="Message `content` must be a string or list of content parts",
                )
            new_messages.append(
                adapt_messages_to_generic_oci_standard_content_message(role, content)
            )

        elif role == "tool":
            if not isinstance(tool_call_id, str):
                raise OCIError(
                    status_code=400,
                    message="Tool result message must have a string `tool_call_id`",
                )
            if not isinstance(content, str):
                raise OCIError(
                    status_code=400,
                    message="Tool result message `content` must be a string",
                )
            new_messages.append(
                adapt_messages_to_generic_oci_standard_tool_response(
                    role, tool_call_id, content
                )
            )

    return new_messages

