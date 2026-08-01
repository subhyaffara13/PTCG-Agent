
def normalize_error_messages(messages: list[str]) -> list[str]:
    """Translate an array of error messages to use / as path separator."""

    a = []
    for m in messages:
        a.append(m.replace(os.sep, "/"))
    return a

