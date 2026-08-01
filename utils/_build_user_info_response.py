
def _build_user_info_response(
    user_id: Optional[str],
    user_info: Optional[Any],
    keys: Optional[List[LiteLLM_VerificationToken]],
    team_list: list[Any],
    teams_1: Optional[list[Any]],
) -> UserInfoResponse:
    """Create UserInfoResponse while filtering sensitive fields."""
    if user_info is None and keys is not None:
        spend = sum(getattr(k, "spend", 0) for k in keys)
        user_info = {"spend": spend}

    returned_keys = _process_keys_for_user_info(keys=keys, all_teams=teams_1)
    team_list.sort(key=lambda x: (getattr(x, "team_alias", "") or ""))

    _user_info = (
        user_info.model_dump() if isinstance(user_info, BaseModel) else user_info
    )
    if isinstance(_user_info, dict):
        _user_info.pop("password", None)

    return UserInfoResponse(
        user_id=user_id,
        user_info=_user_info,
        keys=returned_keys,
        teams=team_list,
    )

