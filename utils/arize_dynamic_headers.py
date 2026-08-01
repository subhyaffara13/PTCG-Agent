
def arize_dynamic_headers(params: StandardCallbackDynamicParams) -> dict[str, str]:
    """Per-request Arize OTLP headers from team/key dynamic params."""
    headers: dict[str, str] = {}
    # ``arize_space_key`` is the suggested param and wins over ``arize_space_id``.
    space = params.get("arize_space_key") or params.get("arize_space_id")
    if space:
        headers["arize-space-id"] = space
    api_key = params.get("arize_api_key")
    if api_key:
        headers["api_key"] = api_key
    return headers

