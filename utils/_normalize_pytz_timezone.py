
def _normalize_pytz_timezone(tz: dt.tzinfo) -> dt.tzinfo:
    """
    If the input tz is a pytz timezone, attempt to convert it to "default"
    tzinfo object (zoneinfo or datetime.timezone).
    """
    if not type(tz).__module__.startswith("pytz"):
        # isinstance(col.dtype.tz, pytz.BaseTzInfo) does not included
        # fixed offsets
        return tz

    if timezones.is_utc(tz):
        return dt.timezone.utc

    if tz.zone is not None:  # type: ignore[attr-defined]
        try:
            return zoneinfo.ZoneInfo(tz.zone)  # type: ignore[attr-defined]
        except Exception:
            # some pytz timezones might not be available for zoneinfo
            pass

    if timezones.is_fixed_offset(tz):
        # Convert pytz fixed offset to datetime.timezone
        try:
            offset = tz.utcoffset(None)
            if offset is not None:
                return dt.timezone(offset)
        except Exception:
            pass

    return tz

