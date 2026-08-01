
def is_deleted_msgid(msgid: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    for explanation, deleted_messages in DELETED_MESSAGES_IDS.items():
        for deleted_message in deleted_messages:
            if msgid == deleted_message.msgid or any(
                msgid == m[0] for m in deleted_message.old_names
            ):
                return explanation
    return None

