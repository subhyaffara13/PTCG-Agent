
def weave_dynamic_headers(params: StandardCallbackDynamicParams) -> dict[str, str]:
    """Per-request Weave OTLP headers from team/key dynamic params."""
    headers: dict[str, str] = {}
    api_key = params.get("wandb_api_key")
    if api_key:
        headers["Authorization"] = _get_weave_authorization_header(api_key=api_key)
    project_id = params.get("weave_project_id")
    if project_id:
        headers["project_id"] = project_id
    return headers

