
def _hash_value(value, field_name: str) -> Optional[str]:
    """Hashes a value and returns a formatted hash string."""
    if value is None:
        return None
    encoded_value = str(value).encode("utf-8")
    hash_object = hashlib.sha512()
    hash_object.update(encoded_value)
    hex_digest = hash_object.hexdigest()
    return f"hashed_{field_name}-{hex_digest}"

