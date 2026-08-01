
def is_moved_symbol(symbol: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    for explanation, moved_messages in MOVED_TO_EXTENSIONS.items():
        for moved_message in moved_messages:
            if symbol == moved_message.symbol or any(
                symbol == m[1] for m in moved_message.old_names
            ):
                return explanation
    return None

