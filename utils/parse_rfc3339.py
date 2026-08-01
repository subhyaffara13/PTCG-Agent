
def parse_rfc3339(string: str) -> datetime | date | time:
    m = RFC_3339_DATETIME.match(string)
    if m:
        year = int(m.group("year"))
        month = int(m.group("month"))
        day = int(m.group("day"))
        hour = int(m.group("hour"))
        minute = int(m.group("minute"))
        second = int(m.group("second") or 0)
        microsecond = 0

        if m.group("fraction"):
            microsecond = int((f"{m.group('fraction'):<06s}")[:6])

        if m.group("tz"):
            # Timezone
            tz = m.group("tz")
            if tz.upper() == "Z":
                tzinfo = _utc
            else:
                sign = tz[0]
                hour_offset, minute_offset = map(int, tz[1:].split(":"))
                offset = timedelta(seconds=hour_offset * 3600 + minute_offset * 60)
                if sign == "-":
                    offset = -offset

                tzinfo = timezone(offset, tz)

            return datetime(
                year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo
            )
        else:
            return datetime(year, month, day, hour, minute, second, microsecond)

    m = RFC_3339_DATE.match(string)
    if m:
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))

        return date(year, month, day)

    m = RFC_3339_TIME.match(string)
    if m:
        hour = int(m.group("hour"))
        minute = int(m.group("minute"))
        second = int(m.group("second") or 0)
        microsecond = 0

        if m.group("fraction"):
            microsecond = int((f"{m.group('fraction'):<06s}")[:6])

        return time(hour, minute, second, microsecond)

    raise ValueError("Invalid RFC 3339 string")

