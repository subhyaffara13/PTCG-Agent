
def _get_value_as_primitive_value(numeric_value):
    """Maps a NumericValue proto to a float or tuple of float."""
    if numeric_value.float_value is not None:
        return numeric_value.float_value
    if numeric_value.date is not None:
        date = numeric_value.date
        value_tuple = [None, None, None]
        # All dates fields are cased to float to produce a simple primitive value.
        if date.year is not None:
            value_tuple[0] = float(date.year)
        if date.month is not None:
            value_tuple[1] = float(date.month)
        if date.day is not None:
            value_tuple[2] = float(date.day)
        return tuple(value_tuple)
    raise ValueError(f"Unknown type: {numeric_value}")

