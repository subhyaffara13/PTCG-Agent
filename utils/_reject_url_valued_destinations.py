from typing import Any, Dict

def _reject_url_valued_destinations(data: Dict[str, Any]) -> None:
    """Reject URL-valued ``model``/``file_id`` unless admin-allowlisted.

    Some providers (HuggingFace, Oobabooga, Gemini files) accept a URL in the
    identifier field and use it as the outbound destination. On the proxy that
    is an SSRF primitive — a low-privilege caller can point traffic at any
    host the proxy can reach, including internal services. Reject here at the
    proxy boundary so SDK users (who legitimately pass URL-valued identifiers)
    are unaffected, while admins can opt specific hosts back in via
    ``litellm.provider_url_destination_allowed_hosts``.
    """
    allowed_hosts = getattr(litellm, "provider_url_destination_allowed_hosts", []) or []
    for field in _URL_DESTINATION_REQUEST_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.startswith(("http://", "https://")):
            continue
        if is_url_destination_allowed_by_host(value, allowed_hosts):
            continue
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_request",
                "param": field,
                "message": (
                    f"URL-valued '{field}' is not allowed. Configure custom "
                    "endpoints with api_base instead, or add the destination "
                    "host to `provider_url_destination_allowed_hosts` in "
                    "litellm_settings."
                ),
            },
        )

