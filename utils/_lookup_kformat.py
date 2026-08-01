
def _lookup_kformat(key_type: utils.Buffer):
    """Return valid format or throw error"""
    if not isinstance(key_type, bytes):
        key_type = memoryview(key_type).tobytes()
    if key_type in _KEY_FORMATS:
        return _KEY_FORMATS[key_type]
    raise UnsupportedAlgorithm(f"Unsupported key type: {key_type!r}")

