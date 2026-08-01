
def _is_safe_cli_sso_scalar_claim_value(value: Any) -> bool:
    if not isinstance(value, _CLI_SSO_SCALAR_TYPES):
        return False
    if isinstance(value, str):
        if len(value) > CLI_SSO_CLAIM_MAX_SCALAR_LENGTH:
            return False
        if value.startswith("eyJ") and value.count(".") >= 2:
            return False
    return True

