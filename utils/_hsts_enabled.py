
def _hsts_enabled() -> bool:
    return os.getenv("LITELLM_ENABLE_HSTS", "false").strip().lower() == "true"

