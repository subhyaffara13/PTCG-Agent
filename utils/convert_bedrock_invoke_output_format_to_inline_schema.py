
def convert_bedrock_invoke_output_format_to_inline_schema(
    output_format: Dict,
    request_body: Dict,
) -> None:
    """
    Embed an Anthropic structured-output schema into the last user message.

    Bedrock Invoke does not support ``output_format`` directly, so the schema is
    appended to the final user message for prompt-engineered structured output.
    The caller's ``messages`` list, message dict, and content list are not
    mutated; a fresh ``messages`` list with a copied final user message is
    written back to ``request_body``.
    """
    schema = output_format.get("schema")
    if not schema:
        return

    messages = request_body.get("messages")
    if not isinstance(messages, list) or not messages:
        return

    last_user_idx = None
    for i in range(len(messages) - 1, -1, -1):
        message = messages[i]
        if isinstance(message, dict) and message.get("role") == "user":
            last_user_idx = i
            break

    if last_user_idx is None:
        return

    original = messages[last_user_idx]
    content = original.get("content", [])
    schema_block = {"type": "text", "text": json.dumps(schema)}
    if isinstance(content, str):
        new_content = [{"type": "text", "text": content}, schema_block]
    elif isinstance(content, list):
        new_content = [*content, schema_block]
    else:
        return

    new_messages = list(messages)
    new_messages[last_user_idx] = {**original, "content": new_content}
    request_body["messages"] = new_messages

