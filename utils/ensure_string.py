
def ensure_string(key):
    if isinstance(key, bytes):
        return key.decode("utf-8")
    elif isinstance(key, str):
        return key
    else:
        raise TypeError("Key must be either a string or bytes")

