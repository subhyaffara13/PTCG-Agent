
def _uses_region_derived_base_url(base_url: str | httpx.URL | None) -> bool:
    if isinstance(base_url, str) and not base_url.strip():
        base_url = None
    if base_url is not None:
        return False

    environment_base_url = os.environ.get("AWS_BEDROCK_BASE_URL")
    return environment_base_url is None or not environment_base_url.strip()

