
def _extract_inbound_headers(
    request_data: dict,
    logging_obj: Optional["LiteLLMLoggingObj"],
    extra_allowlist: Optional[Set[str]] = None,
) -> Optional[Dict[str, str]]:
    """
    Extract inbound headers from available request context.

    We try multiple locations to support different call paths:
    - proxy endpoints: request_data["proxy_server_request"]["headers"]
    - if the guardrail is passed the proxy_server_request object directly
    - metadata headers captured in litellm_pre_call_utils
    - response hooks: fallback to logging_obj.model_call_details
    """
    # 1) Most common path (proxy): full request context in proxy_server_request
    headers = request_data.get("proxy_server_request", {}).get("headers")
    if headers:
        return _sanitize_inbound_headers(headers, extra_allowlist=extra_allowlist)

    # 2) Some guardrails pass proxy_server_request as request_data itself
    headers = request_data.get("headers")
    if headers:
        return _sanitize_inbound_headers(headers, extra_allowlist=extra_allowlist)

    # 3) Pre-call: headers stored in request metadata
    metadata_headers = (request_data.get("metadata") or {}).get("headers")
    if metadata_headers:
        return _sanitize_inbound_headers(
            metadata_headers, extra_allowlist=extra_allowlist
        )

    litellm_metadata_headers = (request_data.get("litellm_metadata") or {}).get(
        "headers"
    )
    if litellm_metadata_headers:
        return _sanitize_inbound_headers(
            litellm_metadata_headers, extra_allowlist=extra_allowlist
        )

    # 4) Post-call: headers not present on response; fallback to logging object
    if logging_obj and getattr(logging_obj, "model_call_details", None):
        try:
            details = logging_obj.model_call_details or {}
            headers = (
                details.get("litellm_params", {})
                .get("metadata", {})
                .get("headers", None)
            )
            if headers:
                return _sanitize_inbound_headers(
                    headers, extra_allowlist=extra_allowlist
                )
        except Exception:
            pass

    return None

