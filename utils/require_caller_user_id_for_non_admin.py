
def require_caller_user_id_for_non_admin(
    user_api_key_dict: UserAPIKeyAuth,
) -> str:
    """Return the caller's user_id, or raise 403 if missing.

    Non-admin analytics endpoints scope queries by the caller's own user_id.
    Service-account keys are deliberately created with user_id=None
    (key_management_endpoints.py forces ``data.user_id = None`` at key
    creation). Without this guard, that None value flows through to the
    daily-activity builder, which treats ``entity_id is None`` as "no filter"
    and returns every tenant's data.

    Callers must check is_admin first; this helper is only valid on the
    non-admin scoping branch.
    """
    if user_api_key_dict.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": (
                    "Service-account keys cannot query user analytics. "
                    "Use a user-bound key, or call as a proxy admin."
                )
            },
        )
    return user_api_key_dict.user_id

