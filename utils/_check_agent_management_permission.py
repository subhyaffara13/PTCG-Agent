
def _check_agent_management_permission(user_api_key_dict: UserAPIKeyAuth) -> None:
    """
    Raises HTTP 403 if the caller does not have permission to create, update,
    or delete agents.  Only PROXY_ADMIN users are allowed to perform these
    write operations.
    """
    if user_api_key_dict.user_role != LitellmUserRoles.PROXY_ADMIN:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Only proxy admins can create, update, or delete agents. Your role={}".format(
                    user_api_key_dict.user_role
                )
            },
        )

