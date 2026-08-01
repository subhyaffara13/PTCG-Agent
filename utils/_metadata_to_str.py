
def _metadata_to_str(key, value):
    """Convert metadata key/value to a form that hyperref accepts."""
    if isinstance(value, datetime.datetime):
        value = _datetime_to_pdf(value)
    elif key == 'Trapped':
        value = value.name.decode('ascii')
    else:
        value = str(value)

    # ensure that metadata does not contain special TeX chars because we
    # insert the metadata as raw text into the TeX source
    invalid_chars = r"\{}[]()"
    if any(c in value + key for c in invalid_chars):
        raise ValueError(
            f"Invalid metadata value for {key!r}: {value!r}. "
            f"The value must not contain the chars {invalid_chars}.")

    return f'{key}={{{value}}}'

