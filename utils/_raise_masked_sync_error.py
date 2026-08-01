
def _raise_masked_sync_error(e: httpx.HTTPStatusError, stream: bool) -> None:
    """Raise a MaskedHTTPStatusError for sync HTTP handlers."""
    if stream:
        try:
            _body = mask_sensitive_info(
                _safe_read_response(
                    e.response,
                    timeout=_STREAMING_ERROR_BODY_READ_TIMEOUT_SECONDS,
                )
            )
            raise MaskedHTTPStatusError(e, message=_body, text=_body) from None
        finally:
            try:
                e.response.close()
            except Exception:
                pass
    _text = mask_sensitive_info(_safe_get_response_text(e.response))
    raise MaskedHTTPStatusError(e, message=_text, text=_text) from None

