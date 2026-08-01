
def _has_openai_credentials() -> bool:
    return _os.environ.get("OPENAI_API_KEY") is not None

