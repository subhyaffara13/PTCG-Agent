
def create_mock_braintrust_client():
    """
    Monkey-patch HTTPHandler.post to intercept Braintrust sync calls.

    Braintrust uses HTTPHandler for sync calls and AsyncHTTPHandler for async calls.
    HTTPHandler.post uses self.client.send(), not self.client.post(), so we need
    custom patching for sync (similar to Helicone).
    AsyncHTTPHandler.post is patched by the factory.

    We use custom patching instead of factory's patch_http_handler because we need
    endpoint-specific responses (different for /project vs /project_logs).

    This function is idempotent - it only initializes mocks once, even if called multiple times.
    """
    global _original_http_handler_post, _mocks_initialized

    if _mocks_initialized:
        return

    verbose_logger.debug("[BRAINTRUST MOCK] Initializing Braintrust mock client...")

    from litellm.llms.custom_httpx.http_handler import HTTPHandler

    if _original_http_handler_post is None:
        _original_http_handler_post = HTTPHandler.post
        HTTPHandler.post = _mock_http_handler_post  # type: ignore
        verbose_logger.debug("[BRAINTRUST MOCK] Patched HTTPHandler.post")

    # CRITICAL: Call the factory's initialization function to patch AsyncHTTPHandler.post
    # This is required for async calls to be mocked
    create_mock_braintrust_factory_client()

    verbose_logger.debug(
        f"[BRAINTRUST MOCK] Mock latency set to {_MOCK_LATENCY_SECONDS*1000:.0f}ms"
    )
    verbose_logger.debug(
        "[BRAINTRUST MOCK] Braintrust mock client initialization complete"
    )

    _mocks_initialized = True

