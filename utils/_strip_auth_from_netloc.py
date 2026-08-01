
def _strip_auth_from_netloc(netloc: str, safe_user_passwords: Collection[str]) -> str:
    if "@" not in netloc:
        return netloc
    user_pass, netloc_no_user_pass = netloc.split("@", 1)
    if user_pass in safe_user_passwords:
        return netloc
    if _PEP610_USER_PASS_ENV_VARS_REGEX.match(user_pass):
        return netloc
    return netloc_no_user_pass


def _strip_auth_from_netloc(netloc: str, safe_user_passwords: Collection[str]) -> str:
    if "@" not in netloc:
        return netloc
    user_pass, netloc_no_user_pass = netloc.split("@", 1)
    if user_pass in safe_user_passwords:
        return netloc
    if _PEP610_USER_PASS_ENV_VARS_REGEX.match(user_pass):
        return netloc
    return netloc_no_user_pass

