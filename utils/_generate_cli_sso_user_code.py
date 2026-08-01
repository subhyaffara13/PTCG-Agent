
def _generate_cli_sso_user_code() -> str:
    user_code = "".join(secrets.choice(_CLI_SSO_USER_CODE_ALPHABET) for _ in range(8))
    return f"{user_code[:4]}-{user_code[4:]}"

