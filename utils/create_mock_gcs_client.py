
def create_mock_gcs_client():
    """
    Monkey-patch AsyncHTTPHandler methods to intercept GCS calls.

    AsyncHTTPHandler is used by LiteLLM's get_async_httpx_client() which is what
    GCSBucketBase uses for making API calls.

    This function is idempotent - it only initializes mocks once, even if called multiple times.
    """
    global _original_async_handler_get, _original_async_handler_delete, _mocks_initialized

    # Use factory for POST handler
    _create_mock_gcs_post()

    # If already initialized, skip GET/DELETE patching
    if _mocks_initialized:
        return

    verbose_logger.debug("[GCS MOCK] Initializing GCS GET/DELETE handlers...")

    # Patch GET and DELETE handlers (GCS-specific)
    from litellm.llms.custom_httpx.http_handler import AsyncHTTPHandler

    if _original_async_handler_get is None:
        _original_async_handler_get = AsyncHTTPHandler.get
        AsyncHTTPHandler.get = _mock_async_handler_get  # type: ignore
        verbose_logger.debug("[GCS MOCK] Patched AsyncHTTPHandler.get")

    if _original_async_handler_delete is None:
        _original_async_handler_delete = AsyncHTTPHandler.delete
        AsyncHTTPHandler.delete = _mock_async_handler_delete  # type: ignore
        verbose_logger.debug("[GCS MOCK] Patched AsyncHTTPHandler.delete")

    verbose_logger.debug(
        f"[GCS MOCK] Mock latency set to {_MOCK_LATENCY_SECONDS*1000:.0f}ms"
    )
    verbose_logger.debug("[GCS MOCK] GCS mock client initialization complete")

    _mocks_initialized = True

