
def key_generation_check(
    team_table: Optional[LiteLLM_TeamTableCachedObj],
    user_api_key_dict: UserAPIKeyAuth,
    data: GenerateKeyRequest,
    route: KeyManagementRoutes,
) -> bool:
    """
    Check if admin has restricted key creation to certain roles for teams or individuals
    """

    ## check if key is for team or individual
    is_team_key = _is_team_key(data=data)
    _is_admin = (
        user_api_key_dict.user_role is not None
        and user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    )
    if is_team_key:
        if team_table is None and litellm.key_generation_settings is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to find team object in database. Team ID: {data.team_id}",
            )
        elif team_table is None:
            if _is_admin:
                return True  # admins can assign team_id without team table
            # Non-admin callers must have a valid team (LIT-1884)
            raise HTTPException(
                status_code=400,
                detail=f"Unable to find team object in database. Team ID: {data.team_id}",
            )
        return _team_key_generation_check(
            team_table=team_table,
            user_api_key_dict=user_api_key_dict,
            data=data,
            route=route,
        )
    else:
        return _personal_key_generation_check(
            user_api_key_dict=user_api_key_dict, data=data
        )

