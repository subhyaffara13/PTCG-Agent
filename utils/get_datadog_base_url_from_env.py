
def get_datadog_base_url_from_env() -> Optional[str]:
    """
    Get base URL override from common DD_BASE_URL env var.
    This is useful for testing or custom endpoints.
    """
    return os.getenv("DD_BASE_URL")

