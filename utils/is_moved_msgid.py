
def is_moved_msgid(msgid: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    for explanation, moved_messages in MOVED_TO_EXTENSIONS.items():
        for moved_message in moved_messages:
            if msgid == moved_message.msgid or any(
                msgid == m[0] for m in moved_message.old_names
            ):
                return explanation
    return None

