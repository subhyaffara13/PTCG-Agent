
def _merge_query_params_into_data(data: dict, request: Request) -> dict:
    """
    For GET/DELETE endpoints that cannot carry a JSON body, read a
    JSON-encoded ``litellm_params_template`` query parameter and merge its
    contents into *data*, without overwriting keys that are already present
    (e.g. path params like ``name`` or the fixed ``custom_llm_provider``).

    This mirrors the ``litellm_params_template`` handling in
    ``create_gemini_agent`` and is the supported way for multi-tenant
    callers to supply per-request credentials on non-POST endpoints:

    .. code-block:: bash

        curl "http://localhost:4000/v1beta/agents?litellm_params_template=%7B%22api_key%22%3A%22AIza...%22%7D" \\
            -H "Authorization: Bearer sk-..."

    Credentials MUST NOT be passed as plain flat query parameters (e.g.
    ``?api_key=AIza...``) because URL query strings appear verbatim in
    web-server access logs, CDN edge logs, browser history, and Referer
    headers. Use the ``litellm_params_template`` JSON body field on POST
    requests, or the JSON-encoded query parameter above for GET/DELETE.
    """
    query_params = _safe_get_request_query_params(request)
    if not query_params:
        return data

    raw_template = query_params.get("litellm_params_template")
    if raw_template:
        try:
            template = (
                json.loads(raw_template)
                if isinstance(raw_template, str)
                else raw_template
            )
        except (json.JSONDecodeError, ValueError):
            template = {}
        if isinstance(template, dict):
            for key, value in template.items():
                data.setdefault(key, value)

    return data

