
def _enforce_caller_supplied_provider_key(
    data: dict,
    user_api_key_dict: UserAPIKeyAuth,
) -> None:
    """
    SECURITY: refuse to use the proxy's shared GOOGLE_API_KEY / GEMINI_API_KEY
    env fallback for non-admin callers on Gemini managed-agent CRUD endpoints.

    These endpoints are part of ``llm_api_routes`` so any authenticated LLM key
    can reach them, but unlike ``/v1beta/models/...:generateContent`` they are
    *not* routed through ``model_list`` — the only credential source is either
    the per-request ``litellm_params_template`` or the env var fallback. Without
    this guard, any ordinary proxy user could list, create, or delete managed
    agents inside the operator's Gemini project using the operator's key.

    Proxy admins (master key) keep the env-fallback convenience for ops use.
    """
    if _is_proxy_admin(user_api_key_dict):
        return
    if data.get("api_key"):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=(
            "Gemini managed-agent endpoints require a caller-supplied "
            "Gemini api_key (via 'litellm_params_template'). Falling back to "
            "the proxy's GOOGLE_API_KEY / GEMINI_API_KEY env vars is only "
            "permitted for proxy admins."
        ),
    )

