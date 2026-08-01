
def dynamic_otlp_headers(
    callback_name: str | None,
    dynamic_params: StandardCallbackDynamicParams | None,
) -> dict[str, str] | None:
    """Per-request OTLP headers for ``callback_name``, or ``None`` if N/A.

    ``None`` means "no per-request routing" — the caller uses its default tracer.
    """
    builder = DYNAMIC_HEADERS_BY_CALLBACK.get(callback_name or "")
    if builder is None or not dynamic_params:
        return None
    headers = builder(dynamic_params)
    return headers or None

