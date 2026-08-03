from typing import Optional

def _enforce_user_info_access(
    user_id: Optional[str], user_api_key_dict: UserAPIKeyAuth
) -> None:
    """Re-validate that the caller may read the resolved ``user_id`` after
    URL-decoding has been finalized.

    The route-level check in ``RouteChecks.non_proxy_admin_allowed_routes_check``
    runs against ``request.query_params``, which decodes a literal ``+`` to a
    space. ``_normalize_user_info_user_id`` then re-parses the raw query with
    ``unquote`` so the endpoint can return rows for user_ids that contain ``+``
    (e.g. plus-addressed emails). That asymmetry let an attacker who registered
    a username with a literal space pass the route check and then read another
    user's row by sending the encoded ``+`` form. Re-checking ownership here
    closes the gap without changing the supported user_id grammar.
    """
    if user_id is None:
        return
    # Only true proxy admin bypasses ownership. PROXY_ADMIN_VIEW_ONLY is
    # subject to the same `user_id == valid_token.user_id` rule that
    # `RouteChecks.non_proxy_admin_allowed_routes_check` applies upstream
    # for the `/user/info` route.
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN:
        return
    if user_id == user_api_key_dict.user_id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=(
            f"key not allowed to access this user's info. user_id={user_id}, "
            f"key's user_id={user_api_key_dict.user_id}"
        ),
    )

