
def _check_passthrough_routes_caller_permission(
    data: BaseModel,
    user_api_key_dict: UserAPIKeyAuth,
    *,
    entity: str = "key",
) -> None:
    """
    Only proxy admins may set `allowed_passthrough_routes` (top-level or under
    `metadata`) — it short-circuits the role-based route gate, so keys and teams
    must be gated identically.
    """
    # view-only admins excluded by design; blocked upstream from writes anyway
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value:
        return
    if getattr(data, "allowed_passthrough_routes", None):
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Only proxy admins can set `allowed_passthrough_routes` on a {entity}."
            },
        )
    metadata = getattr(data, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("allowed_passthrough_routes"):
        raise HTTPException(
            status_code=403,
            detail={
                "error": f"Only proxy admins can set `metadata.allowed_passthrough_routes` on a {entity}."
            },
        )

