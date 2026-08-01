
def _is_valid_cli_sso_user_code(user_code: str | None) -> bool:
    return isinstance(user_code, str) and bool(
        _CLI_SSO_USER_CODE_RE.fullmatch(user_code)
    )

