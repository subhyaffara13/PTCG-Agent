
def detect_provider() -> Provider | None:
    """Detect the CI provider able to mint an OIDC id token, or `None` if not in a supported CI."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return Provider.GITHUB
    return None

