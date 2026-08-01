
def _parse_value(value):
    value = ''.join(value)
    if value != value.strip() or '_' in value:
        raise ValueError(f"Invalid value: {value!r}")
    try:
        return int(value)
    except ValueError:
        return float(value)

