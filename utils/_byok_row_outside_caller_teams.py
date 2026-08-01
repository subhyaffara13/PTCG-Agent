
def _byok_row_outside_caller_teams(
    model_info_dict: Dict[str, Any], allowed_team_ids: Optional[Set[str]]
) -> bool:
    """Whether a team BYOK row belongs to a team the caller is not a member of.

    `team_id` is only set on team BYOK rows; non-team rows fall through
    unaffected. `allowed_team_ids is None` means no scoping (e.g. admins).
    """
    if allowed_team_ids is None:
        return False
    team_id = model_info_dict.get("team_id")
    if team_id is None:
        return False
    return team_id not in allowed_team_ids

