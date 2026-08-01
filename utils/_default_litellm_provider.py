
def _default_litellm_provider(proxy_base_url: str) -> Dict[str, str]:
    return {"organization": "LiteLLM Proxy", "url": proxy_base_url}

