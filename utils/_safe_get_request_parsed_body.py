
def _safe_get_request_parsed_body(request: Optional[Request]) -> Optional[dict]:
    if request is None:
        return None
    if (
        hasattr(request, "scope")
        and "parsed_body" in request.scope
        and isinstance(request.scope["parsed_body"], tuple)
    ):
        accepted_keys, parsed_body = request.scope["parsed_body"]
        return {key: parsed_body[key] for key in accepted_keys}
    return None

