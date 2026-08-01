
def _parse_error(payload: "StandardLoggingPayload") -> SpanError | None:
    """A ``SpanError`` for a failed request, or ``None`` on success."""
    if payload.get("status") != "failure":
        return None
    info = cast(Mapping[str, object], payload.get("error_information") or {})
    return SpanError(
        error_type=as_str(info.get("error_class")) or as_str(info.get("error_code")),
        message=as_str(info.get("error_message")) or as_str(payload.get("error_str")),
    )

