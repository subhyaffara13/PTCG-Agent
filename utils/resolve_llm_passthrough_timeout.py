
def resolve_llm_passthrough_timeout(
    kwargs: Optional[dict] = None,
    litellm_params: Optional[dict] = None,
    router_timeout: Optional[float] = None,
) -> float:
    """
    Resolve upstream httpx timeout for SDK native passthrough (e.g. Bedrock /converse).

    Precedence: kwargs timeout/request_timeout -> litellm_params timeout/request_timeout
    -> router_timeout -> general_settings.pass_through_request_timeout -> 600s default.
    """
    kwargs = kwargs or {}
    litellm_params = litellm_params or {}

    for source in (kwargs, litellm_params):
        for key in ("timeout", "request_timeout"):
            val = source.get(key)
            if val is not None:
                return float(val)

    if router_timeout is not None:
        return float(router_timeout)

    return resolve_pass_through_request_timeout()

