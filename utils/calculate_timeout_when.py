
def calculate_timeout_when(
    loop_time: float,
    timeout: float,
    timeout_ceiling_threshold: float,
) -> float:
    """Calculate when to execute a timeout."""
    when = loop_time + timeout
    if timeout > timeout_ceiling_threshold:
        return ceil(when)
    return when

