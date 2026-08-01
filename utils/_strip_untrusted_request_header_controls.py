
def _strip_untrusted_request_header_controls(
    headers: Any,
    *,
    allow_client_message_redaction_opt_out: bool = False,
) -> None:
    if not isinstance(headers, dict):
        return

    for header_name in list(headers.keys()):
        if (
            isinstance(header_name, str)
            and header_name.lower() in _UNTRUSTED_REQUEST_HEADER_CONTROL_FIELDS
        ):
            if allow_client_message_redaction_opt_out:
                continue
            headers.pop(header_name, None)

