
def _allow_public_health_readiness_details() -> bool:
    from litellm.proxy.proxy_server import general_settings

    return general_settings.get("allow_public_health_readiness_details") is True

