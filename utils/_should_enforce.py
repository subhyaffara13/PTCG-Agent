
def _should_enforce():
    enforce = os.getenv("SETUPTOOLS_ENFORCE_DEPRECATION", "false").lower()
    return enforce in ("true", "on", "ok", "1")

