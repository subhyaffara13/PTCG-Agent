
def _is_valid_cli_sso_login_id(login_id: Optional[str]) -> bool:
    return isinstance(login_id, str) and bool(_CLI_SSO_LOGIN_ID_RE.fullmatch(login_id))

