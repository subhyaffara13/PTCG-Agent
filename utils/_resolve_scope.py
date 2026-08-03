from typing import Optional

def _resolve_scope(
    user_api_key_dict: UserAPIKeyAuth,
    requested_user_id: Optional[str],
    requested_team_id: Optional[str],
) -> tuple[Optional[str], Optional[str]]:
    """
    Resolve the (user_id, team_id) to stamp on a new row.

    - PROXY_ADMIN: may override either dimension via the request body.
    - Everyone else: the requested values must match their own (or be omitted).

    Also rejects identity-less creation: a row with both user_id and team_id
    NULL is invisible to every non-admin caller (the visibility filter would
    never match it), so we refuse to create orphan rows unless the caller is
    a PROXY_ADMIN who is explicitly stamping a global/shared row.
    """
    if _is_admin(user_api_key_dict):
        user_id = (
            requested_user_id
            if requested_user_id is not None
            else user_api_key_dict.user_id
        )
        team_id = (
            requested_team_id
            if requested_team_id is not None
            else user_api_key_dict.team_id
        )
        return user_id, team_id

    if requested_user_id is not None and requested_user_id != user_api_key_dict.user_id:
        raise HTTPException(
            status_code=403,
            detail="Only proxy admins may set user_id to a different user.",
        )
    if requested_team_id is not None and requested_team_id != user_api_key_dict.team_id:
        raise HTTPException(
            status_code=403,
            detail="Only proxy admins may set team_id to a different team.",
        )
    user_id = user_api_key_dict.user_id
    team_id = user_api_key_dict.team_id
    if not user_id and not team_id:
        # Orphan row: no user_id and no team_id means no non-admin can ever
        # see it again via the visibility filter. Reject up front.
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot create a memory entry without a user_id or team_id. "
                "Authenticate with a key that has a user_id or team_id, or call "
                "as a proxy admin."
            ),
        )
    return user_id, team_id

