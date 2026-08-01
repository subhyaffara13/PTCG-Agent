
def is_non_content_values_set(message: AllMessageValues) -> bool:
    ignore_keys = ["content", "role", "name"]
    return any(
        message.get(key, None) is not None for key in message if key not in ignore_keys
    )

