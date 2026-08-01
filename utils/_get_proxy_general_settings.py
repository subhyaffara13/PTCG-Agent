
def _get_proxy_general_settings() -> Dict[str, Any]:
    try:
        from litellm.proxy.proxy_server import general_settings

        return general_settings or {}
    except ImportError:
        return {}

