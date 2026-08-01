
def _get_gcs_metadata_http_handler() -> HTTPHandler:
    global _GCS_METADATA_HTTP_HANDLER
    if _GCS_METADATA_HTTP_HANDLER is None:
        _GCS_METADATA_HTTP_HANDLER = HTTPHandler(timeout=5.0)
    return _GCS_METADATA_HTTP_HANDLER

