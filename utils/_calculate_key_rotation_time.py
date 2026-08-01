
def _calculate_key_rotation_time(rotation_interval: str) -> datetime:
    """
    Helper function to calculate the next rotation time for a key based on the rotation interval.

    Args:
        rotation_interval: String representing the rotation interval (e.g., '30d', '90d', '1h')

    Returns:
        datetime: The calculated next rotation time in UTC
    """
    now = datetime.now(timezone.utc)
    interval_seconds = duration_in_seconds(rotation_interval)
    return now + timedelta(seconds=interval_seconds)

