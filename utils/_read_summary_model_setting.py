
def _read_summary_model_setting() -> Optional[str]:
    """Look up the configured summarization model from proxy general_settings."""
    try:
        from litellm.proxy.proxy_server import general_settings
    except Exception:
        return None
    value = general_settings.get(COMPACT_SUMMARY_MODEL_SETTING_KEY)
    return value if isinstance(value, str) and value else None

