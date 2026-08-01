
def user_api_key_has_admin_view(user_api_key_dict: UserAPIKeyAuth) -> bool:
    """Return True if the caller's role grants unscoped read access to all
    tenant resources (managed files, batches, vector stores, spend rows, etc).

    Lives on _types.py so leaf modules (e.g. litellm.llms.base_llm.managed_resources)
    can use it without pulling in litellm.proxy.utils via management_endpoints.
    """
    return user_api_key_dict.user_role in (
        LitellmUserRoles.PROXY_ADMIN,
        LitellmUserRoles.PROXY_ADMIN_VIEW_ONLY,
    )

