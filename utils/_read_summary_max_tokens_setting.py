
def _read_summary_max_tokens_setting() -> int:
    """Look up the configured summary ``max_tokens`` from proxy general_settings.

    Falls back to :data:`COMPACT_SUMMARY_MAX_TOKENS` when the setting is
    missing or invalid (non-positive int, wrong type). Operators tune this
    when the default doesn't fit their chosen summary model's output budget.
    """
    try:
        from litellm.proxy.proxy_server import general_settings
    except Exception:
        return COMPACT_SUMMARY_MAX_TOKENS
    value = general_settings.get(COMPACT_SUMMARY_MAX_TOKENS_SETTING_KEY)
    if isinstance(value, int) and value > 0:
        return value
    return COMPACT_SUMMARY_MAX_TOKENS

