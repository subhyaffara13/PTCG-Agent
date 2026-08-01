
def _sanitize_user_agent_token(value: str) -> str:
    if not value:
        return ""
    return "".join(ch if (ch.isalnum() or ch in "-_./") else "_" for ch in value)

