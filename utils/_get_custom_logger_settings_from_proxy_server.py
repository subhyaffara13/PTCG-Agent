from typing import Dict

def _get_custom_logger_settings_from_proxy_server(callback_name: str) -> Dict:
    """
    Get the settings for a custom logger from the proxy server config.yaml

    Proxy server config.yaml defines callback_settings as:

    callback_settings:
        otel:
            message_logging: False
    """
    if litellm.callback_settings:
        return dict(litellm.callback_settings.get(callback_name, {}))
    return {}

