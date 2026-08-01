
def to_yyyy_mm_dd(
    s: Union[str, int, float, None],
    *,
    dayfirst: bool = False,
    yearfirst: bool = False,
) -> Optional[str]:
    """
    Convert a string/int/float to YYYY-MM-DD; return None if parsing fails.
    """
    if not s:
        return None

    s = str(s).strip()

    # Handle Unix timestamps (seconds or milliseconds).
    if _UNIX_TIMESTAMP.match(s):
        try:
            ts_float = float(s)
            # Treat large values as milliseconds.
            if ts_float > 1e11 or ts_float < -1e11:
                ts_float /= 1000.0
            return datetime.fromtimestamp(ts_float, tz=timezone.utc).date().isoformat()
        except Exception:
            return None

    # If it looks like YYYY-M-D (ISO-ish), force yearfirst to avoid surprises.
    try:
        if _ISO_YMD.match(s):
            dt = parser.parse(s, yearfirst=True, dayfirst=False, fuzzy=True)
        else:
            dt = parser.parse(s, yearfirst=yearfirst, dayfirst=dayfirst, fuzzy=True)
        return dt.date().isoformat()
    except Exception:
        return None

