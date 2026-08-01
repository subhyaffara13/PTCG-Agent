
def _normalize_datetime_for_sorting(dt: Any) -> Optional[datetime]:
    """
    Normalize a datetime value to a timezone-aware UTC datetime for sorting.

    This function handles:
    - None values: returns None
    - String values: parses ISO format strings and converts to UTC-aware datetime
    - Datetime objects: converts naive datetimes to UTC-aware, and aware datetimes to UTC

    Args:
        dt: Datetime value (None, str, or datetime object)

    Returns:
        UTC-aware datetime object, or None if input is None or cannot be parsed
    """
    if dt is None:
        return None

    if isinstance(dt, str):
        try:
            # Handle ISO format strings, including 'Z' suffix
            dt_str = dt.replace("Z", "+00:00") if dt.endswith("Z") else dt
            parsed_dt = datetime.fromisoformat(dt_str)
            # Ensure it's UTC-aware
            if parsed_dt.tzinfo is None:
                parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)
            else:
                parsed_dt = parsed_dt.astimezone(timezone.utc)
            return parsed_dt
        except (ValueError, AttributeError):
            return None

    if isinstance(dt, datetime):
        # If naive, assume UTC and make it aware
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        # If aware, convert to UTC
        return dt.astimezone(timezone.utc)

    return None

