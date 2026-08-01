
def _require_admin_view(user_api_key_dict: UserAPIKeyAuth) -> None:
    """Admin Viewer parity: PROXY_ADMIN or PROXY_ADMIN_VIEW_ONLY may read."""
    from litellm.proxy.management_endpoints.common_utils import _user_has_admin_view

    if not _user_has_admin_view(user_api_key_dict):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": CommonProxyErrors.not_allowed_access.value},
        )

