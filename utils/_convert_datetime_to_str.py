
def _convert_datetime_to_str(value: Union[datetime, str, None]) -> Union[str, None]:
    """
    Convert datetime object to ISO format string.

    Args:
        value: datetime object, string, or None

    Returns:
        ISO format string or original value if already string or None
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return value

