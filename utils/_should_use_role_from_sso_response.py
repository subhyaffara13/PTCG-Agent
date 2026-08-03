from typing import Optional

def _should_use_role_from_sso_response(sso_role: Optional[str]) -> bool:
    """returns true if SSO upsert should use the 'role' defined on the SSO response"""
    if sso_role is None:
        return False

    if not is_valid_litellm_user_role(sso_role):
        verbose_proxy_logger.debug(
            f"SSO role '{sso_role}' is not a valid LiteLLM user role. "
            "Ignoring role from SSO response. See LitellmUserRoles enum for valid roles."
        )
        return False
    return True

