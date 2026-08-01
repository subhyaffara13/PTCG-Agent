
def _status_emoji(status: bool | None) -> str:
    if status is None:
        return "⚪"
    return "✅" if status else "❌"

