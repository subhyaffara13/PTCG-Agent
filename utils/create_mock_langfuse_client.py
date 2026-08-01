
def create_mock_langfuse_client():
    """Create and return an httpx.Client instance - the monkey-patch intercepts all calls."""
    _create_mock_langfuse_client_internal()
    return httpx.Client()

