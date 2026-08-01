
def _check_allowed_routes_caller_permission(
    allowed_routes: Optional[list],
    user_api_key_dict: UserAPIKeyAuth,
    *,
    allow_safe_presets: bool = False,
) -> None:
    """
    Only proxy admins may set `allowed_routes` on a key.

    `allowed_routes` overrides the standard role-based route gate in
    RouteChecks.non_proxy_admin_allowed_routes_check, so the field is
    restricted to admins. Non-admins must instead use `key_type` to pick a
    preset bucket — that path goes through `handle_key_type` and re-enters
    this function with `allow_safe_presets=True`, which lets the derived
    `llm_api_routes` / `info_routes` values through. Raw-body call sites
    leave `allow_safe_presets=False` so non-admins can't write those values
    directly.
    """
    # Empty list is the default on GenerateKeyRequest — treat as "not set".
    if not allowed_routes:
        return
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value:
        return
    if allow_safe_presets and all(
        r in _NON_ADMIN_SAFE_ALLOWED_ROUTES_PRESETS for r in allowed_routes
    ):
        return
    raise HTTPException(
        status_code=403,
        detail={
            "error": (
                "Only proxy admins can set `allowed_routes` on a key. "
                "Use `key_type` to pick a preset route bucket instead."
            )
        },
    )

