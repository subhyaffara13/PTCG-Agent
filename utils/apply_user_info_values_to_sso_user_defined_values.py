
def apply_user_info_values_to_sso_user_defined_values(
    user_info: Optional[Union[LiteLLM_UserTable, NewUserResponse]],
    user_defined_values: Optional[SSOUserDefinedValues],
) -> Optional[SSOUserDefinedValues]:
    if user_defined_values is None:
        return None
    if user_info is not None and user_info.user_id is not None:
        user_defined_values["user_id"] = user_info.user_id

    # SSO role takes precedence - only use DB role if SSO didn't provide one
    # This ensures SSO is the authoritative source for user roles
    sso_role = user_defined_values.get("user_role")
    db_role = user_info.user_role if user_info else None

    if _should_use_role_from_sso_response(sso_role):
        # SSO provided a valid role, keep it and log that we're using it
        verbose_proxy_logger.info(
            f"Using SSO role: {sso_role} (DB role was: {db_role})"
        )
    else:
        # SSO didn't provide a valid role, fall back to DB role or default
        if user_info is None or user_info.user_role is None:
            user_defined_values["user_role"] = (
                LitellmUserRoles.INTERNAL_USER_VIEW_ONLY.value
            )
            verbose_proxy_logger.debug(
                "No SSO or DB role found, using default: INTERNAL_USER_VIEW_ONLY"
            )
        else:
            user_defined_values["user_role"] = user_info.user_role
            verbose_proxy_logger.debug(f"Using DB role: {user_info.user_role}")

    # Preserve the user's existing models from the database
    if user_info is not None and hasattr(user_info, "models") and user_info.models:
        user_defined_values["models"] = user_info.models

    return user_defined_values

