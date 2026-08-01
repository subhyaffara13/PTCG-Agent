
def _normalize_cli_sso_user_code(user_code: str) -> str:
    return "".join(ch for ch in user_code.upper() if ch.isalnum())

