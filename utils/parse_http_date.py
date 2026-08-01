
def parse_http_date(date_str: str | None) -> datetime.datetime | None:
    """Process a date string, return a datetime object"""
    if date_str is not None:
        timetuple = parsedate(date_str)
        if timetuple is not None:
            with suppress(ValueError):
                return datetime.datetime(*timetuple[:6], tzinfo=datetime.timezone.utc)
    return None

