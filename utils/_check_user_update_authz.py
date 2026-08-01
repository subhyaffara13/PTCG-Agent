
def _check_user_update_authz(
    user_request: UpdateUserRequest,
    user_api_key_dict: UserAPIKeyAuth,
    existing_user_row: Optional[BaseModel],
) -> None:
    """Authorization checks for /user/update — raises HTTPException on failure."""
    if (
        user_request.user_role is not None
        and user_api_key_dict.user_role != LitellmUserRoles.PROXY_ADMIN.value
    ):
        raise HTTPException(
            status_code=403, detail="Only proxy admins can modify user roles."
        )

    if existing_user_row is not None:
        typed_row = LiteLLM_UserTable(**existing_user_row.model_dump(exclude_none=True))
        if not can_user_call_user_update(
            user_api_key_dict=user_api_key_dict, user_info=typed_row
        ):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "User does not have permission to update this user. Only PROXY_ADMIN can update other users."
                },
            )
    elif user_api_key_dict.user_role != LitellmUserRoles.PROXY_ADMIN.value:
        # Silent-create guard: only PROXY_ADMIN may create via /user/update.
        raise HTTPException(
            status_code=404,
            detail={
                "error": "User not found. Only PROXY_ADMIN can create users via /user/update; use /user/new instead."
            },
        )

