
def _team_key_generation_check(
    team_table: LiteLLM_TeamTableCachedObj,
    user_api_key_dict: UserAPIKeyAuth,
    data: GenerateKeyRequest,
    route: KeyManagementRoutes,
):
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value:
        return True
    if (
        litellm.key_generation_settings is not None
        and "team_key_generation" in litellm.key_generation_settings
    ):
        _team_key_generation = litellm.key_generation_settings["team_key_generation"]
    else:
        _team_key_generation = TeamUIKeyGenerationConfig(
            allowed_team_member_roles=["admin", "user"],
        )

    _team_key_operation_team_member_check(
        assigned_user_id=data.user_id,
        team_table=team_table,
        user_api_key_dict=user_api_key_dict,
        team_key_generation=_team_key_generation,
        route=route,
    )
    _key_generation_required_param_check(
        data,
        _team_key_generation.get("required_params"),
    )

    # Field-level opt-in: non-admin members may only assign access groups when
    # the team has enabled KEY_ACCESS_GROUP_ASSIGNMENT.
    TeamMemberPermissionChecks.enforce_member_can_assign_access_groups(
        user_api_key_dict=user_api_key_dict,
        team_table=team_table,
        access_group_ids=data.access_group_ids,
    )

    return True

