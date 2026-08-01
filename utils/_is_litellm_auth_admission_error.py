
def _is_litellm_auth_admission_error(exc: Exception) -> bool:
    if isinstance(exc, HTTPException):
        return exc.status_code == 401
    if isinstance(exc, ProxyException):
        try:
            return int(exc.code) == 401
        except (TypeError, ValueError):
            return False
    return False

