
def map_system_message_pt(messages: list) -> list:
    """
    Convert 'system' message to 'user' message if provider doesn't support 'system' role.

    Enabled via `completion(...,supports_system_message=False)`

    If next message is a user message or assistant message -> merge system prompt into it

    if next message is system -> append a user message instead of the system message
    """

    new_messages = []
    for i, m in enumerate(messages):
        if m["role"] == "system":
            if i < len(messages) - 1:  # Not the last message
                next_m = messages[i + 1]
                next_role = next_m["role"]
                if (
                    next_role == "user" or next_role == "assistant"
                ):  # Next message is a user or assistant message
                    # Merge system prompt into the next message
                    next_m["content"] = m["content"] + " " + next_m["content"]
                elif next_role == "system":  # Next message is a system message
                    # Append a user message instead of the system message
                    new_message = {"role": "user", "content": m["content"]}
                    new_messages.append(new_message)
            else:  # Last message
                new_message = {"role": "user", "content": m["content"]}
                new_messages.append(new_message)
        else:  # Not a system message
            new_messages.append(m)

    return new_messages

