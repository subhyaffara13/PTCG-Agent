
def _get_litellm_version() -> str:
    try:
        from importlib.metadata import version

        return version("litellm")
    except Exception:
        return "0.0.0"

