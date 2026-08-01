
def _parse_date(text):
    """Attempts to format a text as a standard date string (yyyy-mm-dd)."""
    text = re.sub(r"Sept\b", "Sep", text)
    for in_pattern, mask, regex in _PROCESSED_DATE_PATTERNS:
        if not regex.match(text):
            continue
        try:
            date = datetime.datetime.strptime(text, in_pattern).date()
        except ValueError:
            continue
        try:
            return _get_numeric_value_from_date(date, mask)
        except ValueError:
            continue
    return None


def _parse_date(datestr: str) -> DatetimeNaTType:
    """Given a date in xport format, return Python date."""
    try:
        # e.g. "16FEB11:10:07:55"
        return datetime.strptime(datestr, "%d%b%y:%H:%M:%S")
    except ValueError:
        return pd.NaT


def _parse_date(value: str | None) -> str | None:
    """Parse date option, converting 'today' to current date."""
    if value is None:
        return None
    if value.lower() == "today":
        return datetime.date.today().isoformat()
    return value

