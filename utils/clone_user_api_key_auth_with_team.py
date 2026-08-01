
def clone_user_api_key_auth_with_team(
    user_api_key_auth: UserAPIKeyAuth,
    team_id: str,
) -> UserAPIKeyAuth:
    """Return a deep copy of the auth context with a different team id."""

    try:
        cloned_auth = user_api_key_auth.model_copy()
    except AttributeError:
        cloned_auth = user_api_key_auth.copy()  # type: ignore[attr-defined]
    cloned_auth.team_id = team_id
    return cloned_auth

