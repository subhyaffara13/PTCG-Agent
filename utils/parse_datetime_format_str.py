import re

def parse_datetime_format_str(format_str, data) -> pd.Series | np.ndarray:
    """Parse datetime `format_str` to interpret the `data`."""
    # timestamp 'ts{unit}:tz'
    timestamp_meta = re.match(r"ts([smun]):(.*)", format_str)
    if timestamp_meta:
        unit, tz = timestamp_meta.group(1), timestamp_meta.group(2)
        if unit != "s":
            # the format string describes only a first letter of the unit, so
            # add one extra letter to convert the unit to numpy-style:
            # 'm' -> 'ms', 'u' -> 'us', 'n' -> 'ns'
            unit += "s"
        data = data.astype(f"datetime64[{unit}]")
        if tz != "":
            data = pd.Series(data).dt.tz_localize("UTC").dt.tz_convert(tz)
        return data

    # date 'td{Days/Ms}'
    date_meta = re.match(r"td([Dm])", format_str)
    if date_meta:
        unit = date_meta.group(1)
        if unit == "D":
            # NumPy doesn't support DAY unit, so converting days to seconds
            # (converting to uint64 to avoid overflow)
            data = (data.astype(np.uint64) * (24 * 60 * 60)).astype("datetime64[s]")
        elif unit == "m":
            data = data.astype("datetime64[ms]")
        else:
            raise NotImplementedError(f"Date unit is not supported: {unit}")
        return data

    raise NotImplementedError(f"DateTime kind is not supported: {format_str}")

