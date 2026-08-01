
def _team_obj_from_token(valid_token: UserAPIKeyAuth) -> LiteLLM_TeamTableCachedObj:
    """Reconstruct a cached team object from the fields already on the
    UserAPIKeyAuth. Only called when valid_token.team_id is known to be
    non-None (the caller gates on it)."""
    assert valid_token.team_id is not None
    return LiteLLM_TeamTableCachedObj(
        team_id=valid_token.team_id,
        max_budget=valid_token.team_max_budget,
        soft_budget=valid_token.team_soft_budget,
        spend=valid_token.team_spend,
        tpm_limit=valid_token.team_tpm_limit,
        rpm_limit=valid_token.team_rpm_limit,
        blocked=valid_token.team_blocked,
        models=valid_token.team_models,
        metadata=valid_token.team_metadata,
        object_permission_id=valid_token.team_object_permission_id,
    )

