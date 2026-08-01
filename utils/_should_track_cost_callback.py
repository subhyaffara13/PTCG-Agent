
def _should_track_cost_callback(
    user_api_key: Optional[str],
    user_id: Optional[str],
    team_id: Optional[str],
    end_user_id: Optional[str],
) -> bool:
    """
    Determine if the cost callback should be tracked based on the kwargs
    """

    # don't run track cost callback if user opted into disabling spend
    if ProxyUpdateSpend.disable_spend_updates() is True:
        return False

    if (
        user_api_key is not None
        or user_id is not None
        or team_id is not None
        or end_user_id is not None
    ):
        return True
    return False

