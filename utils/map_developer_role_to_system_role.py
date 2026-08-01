
def map_developer_role_to_system_role(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    """
    Translate `developer` role to `system` role for non-OpenAI providers.
    """
    new_messages: List[AllMessageValues] = []
    for m in messages:
        if m["role"] == "developer":
            verbose_logger.debug(
                "Translating developer role to system role for non-OpenAI providers."
            )  # ensure user knows what's happening with their input.
            new_messages.append({"role": "system", "content": m["content"]})
        else:
            new_messages.append(m)
    return new_messages

