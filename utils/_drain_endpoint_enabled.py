
def _drain_endpoint_enabled() -> bool:
    from litellm.proxy.proxy_server import general_settings

    return general_settings.get("enable_drain_endpoint") is True

