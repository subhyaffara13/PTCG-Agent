
def _is_valid_endpoint(endpoint) -> bool:
    """
    Helper for interval_range to check if start/end are valid types.
    """
    return any(
        [
            is_number(endpoint),
            isinstance(endpoint, Timestamp),
            isinstance(endpoint, Timedelta),
            endpoint is None,
        ]
    )

