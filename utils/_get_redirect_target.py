
def _get_redirect_target(request: "fastapi.Request", default_target: str = "/") -> str:
    return request.query_params.get("_target_url", default_target)

