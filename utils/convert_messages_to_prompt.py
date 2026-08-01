
def convert_messages_to_prompt(messages: List[AllMessageValues]) -> str:
    """
    Convert OpenAI messages to a single prompt string for A2A agent.

    Formats each message as "{role}: {content}" and joins with newlines
    to preserve conversation history. Handles both string and list content.

    Args:
        messages: List of OpenAI-format messages

    Returns:
        Formatted prompt string with full conversation context
    """
    conversation_parts = []
    for msg in messages:
        # Use LiteLLM's helper to extract text from content (handles both str and list)
        content_text = convert_content_list_to_str(message=msg)

        # Get role
        if isinstance(msg, BaseModel):
            role = msg.model_dump().get("role", "user")
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
        else:
            role = dict(msg).get("role", "user")  # type: ignore

        if content_text:
            conversation_parts.append(f"{role}: {content_text}")

    return "\n".join(conversation_parts)

