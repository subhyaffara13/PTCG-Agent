
def _get_tz(tz: tzinfo) -> str | tzinfo:
    """for a tz-aware type, return an encoded zone"""
    zone = timezones.get_timezone(tz)
    return zone

