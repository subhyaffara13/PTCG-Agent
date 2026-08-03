from typing import Optional

def _team_key_operation_team_member_check(
    assigned_user_id: Optional[str],
    team_table: LiteLLM_TeamTableCachedObj,
    user_api_key_dict: UserAPIKeyAuth,
    team_key_generation: TeamUIKeyGenerationConfig,
    route: KeyManagementRoutes,
):
    if assigned_user_id is not None:
        key_assigned_user_in_team = _get_user_in_team(
            team_table=team_table, user_id=assigned_user_id
        )

        if key_assigned_user_in_team is None:
            raise HTTPException(
                status_code=400,
                detail=f"User={assigned_user_id} not assigned to team={team_table.team_id}",
            )

    team_member_object = _get_user_in_team(
        team_table=team_table, user_id=user_api_key_dict.user_id
    )

    is_admin = (
        user_api_key_dict.user_role is not None
        and user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    )

    if is_admin:
        return True
    elif team_member_object is None:
        raise HTTPException(
            status_code=400,
            detail=f"User={user_api_key_dict.user_id} not assigned to team={team_table.team_id}",
        )
    elif (
        "allowed_team_member_roles" in team_key_generation
        and team_member_object.role
        not in team_key_generation["allowed_team_member_roles"]
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Team member role {team_member_object.role} not in allowed_team_member_roles={team_key_generation['allowed_team_member_roles']}",
        )

    TeamMemberPermissionChecks.does_team_member_have_permissions_for_endpoint(
        team_member_object=team_member_object,
        team_table=team_table,
        route=route,
    )
    return True

