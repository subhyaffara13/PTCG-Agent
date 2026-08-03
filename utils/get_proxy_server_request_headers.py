from typing import Optional

def get_proxy_server_request_headers(litellm_params: Optional[dict]) -> dict:
    """
    Get the `proxy_server_request` headers from the litellm_params.\

    Use this if you want to access the request headers made to LiteLLM proxy server.
    """
    if litellm_params is None:
        return {}

    proxy_request_headers = (litellm_params.get("proxy_server_request") or {}).get(
        "headers"
    ) or {}

    return proxy_request_headers

