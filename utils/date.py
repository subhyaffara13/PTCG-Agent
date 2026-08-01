
def date(raw: str) -> Date:
    """Create a TOML date."""
    value = parse_rfc3339(raw)
    if not isinstance(value, _datetime.date):
        raise ValueError("date() only accepts date strings.")

    return item(value)

