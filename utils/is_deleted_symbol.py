
def is_deleted_symbol(symbol: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    for explanation, deleted_messages in DELETED_MESSAGES_IDS.items():
        for deleted_message in deleted_messages:
            if symbol == deleted_message.symbol or any(
                symbol == m[1] for m in deleted_message.old_names
            ):
                return explanation
    return None

