
def _cli_sso_verification_uri_complete_enabled() -> bool:
    from litellm.proxy.proxy_server import general_settings

    return bool(general_settings.get("allow_cli_sso_verification_uri_complete", False))

