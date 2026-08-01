
def _ensure_encoding(encoding: str | None) -> str:
    # set the encoding if we need
    if encoding is None:
        encoding = _default_encoding

    return encoding

