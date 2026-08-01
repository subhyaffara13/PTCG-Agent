
def _parse_timestamp(timestamp):
    timestamp = ''.join(timestamp)
    if not timestamp:
        return None
    if timestamp != timestamp.strip() or '_' in timestamp:
        raise ValueError(f"Invalid timestamp: {timestamp!r}")
    try:
        # Simple int.
        return Timestamp(int(timestamp), 0)
    except ValueError:
        try:
            # aaaa.bbbb. Nanosecond resolution supported.
            parts = timestamp.split('.', 1)
            return Timestamp(int(parts[0]), int(parts[1][:9].ljust(9, "0")))
        except ValueError:
            # Float.
            ts = float(timestamp)
            if math.isnan(ts) or math.isinf(ts):
                raise ValueError(f"Invalid timestamp: {timestamp!r}")
            return ts

