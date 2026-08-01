
def _get_customer_id_from_standard_headers(
    request_headers: Optional[dict],
) -> Optional[str]:
    """
    Check standard customer ID headers for a customer/end-user ID.

    This enables tools like Claude Code to pass customer IDs via ANTHROPIC_CUSTOM_HEADERS.
    No configuration required - these headers are always checked.

    Args:
        request_headers: The request headers dict

    Returns:
        The customer ID if found in standard headers, None otherwise
    """
    if request_headers is None:
        return None

    for standard_header in STANDARD_CUSTOMER_ID_HEADERS:
        for header_name, header_value in request_headers.items():
            if header_name.lower() == standard_header.lower():
                user_id_str = _coerce_user_id_to_str(header_value)
                if user_id_str:
                    return user_id_str
    return None

