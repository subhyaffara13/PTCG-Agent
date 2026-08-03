from typing import Optional, Union

def _build_sso_user_update_data(
    result: Optional[Union["CustomOpenID", OpenID, dict]],
    user_email: Optional[str],
    user_id: Optional[str],
) -> dict:
    """
    Build the update data dictionary for SSO user upsert.

    Args:
        result: The SSO response containing user information
        user_email: The user's email from SSO
        user_id: The user's ID for logging purposes

    Returns:
        dict: Update data containing user_email and optionally user_role if valid
    """
    update_data: dict = {"user_email": normalize_email(user_email)}

    # Get SSO role from result and include if valid
    sso_role = getattr(result, "user_role", None)
    if sso_role is not None:
        # Convert enum to string if needed
        sso_role_str = (
            sso_role.value if isinstance(sso_role, LitellmUserRoles) else sso_role
        )

        # Only include if it's a valid LiteLLM role
        if _should_use_role_from_sso_response(sso_role_str):
            update_data["user_role"] = sso_role_str
            verbose_proxy_logger.info(
                f"Updating user {user_id} role from SSO: {sso_role_str}"
            )

    return update_data

