
def decode_field_value(value, key=None, field_encodings=None):
    """Decode a field value respecting optional per-field encoding overrides.

    - If *field_encodings* is provided and *key* is in it, the corresponding
      encoding is used (``None`` means keep raw bytes).
    - Otherwise falls back to :func:`str_if_bytes`.
    """
    if not isinstance(value, bytes):
        return value
    if field_encodings and key is not None and key in field_encodings:
        encoding = field_encodings[key]
        if encoding is None:
            return value
        return value.decode(encoding, "replace")
    return str_if_bytes(value)

