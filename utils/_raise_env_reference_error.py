
def _raise_env_reference_error(param: str, *, source: str) -> None:
    raise ValueError(
        f"Callback param '{param}' (from {source}) contains an 'os.environ/' "
        "reference. Environment references in request-supplied parameters are "
        "no longer resolved server-side for security reasons.\n"
        "To resolve:\n"
        "  1. Remove the 'os.environ/' reference from your request body / "
        "metadata.\n"
        "  2. Either (a) configure this callback value in your proxy "
        "config.yaml under 'litellm_settings' / 'general_settings', or "
        "(b) pass the resolved secret value directly in the request.\n"
        "See https://docs.litellm.ai/docs/proxy/logging for server-side "
        "callback configuration."
    )

