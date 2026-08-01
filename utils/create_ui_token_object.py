
def create_ui_token_object(
    login_result: LoginResult,
    general_settings: dict,
    premium_user: bool,
) -> ReturnedUITokenObject:
    """
    Create a ReturnedUITokenObject from a LoginResult.

    Args:
        login_result: The result from authenticate_user
        general_settings: General proxy settings dictionary
        premium_user: Whether premium features are enabled

    Returns:
        ReturnedUITokenObject: Token object ready for JWT encoding
    """
    disabled_non_admin_personal_key_creation = (
        get_disabled_non_admin_personal_key_creation()
    )

    return ReturnedUITokenObject(
        user_id=login_result.user_id,
        key=login_result.key,
        user_email=login_result.user_email,
        user_role=login_result.user_role,
        login_method=login_result.login_method,
        premium_user=premium_user,
        auth_header_name=general_settings.get(
            "litellm_key_header_name", "Authorization"
        ),
        disabled_non_admin_personal_key_creation=disabled_non_admin_personal_key_creation,
        server_root_path=get_server_root_path(),
    )

