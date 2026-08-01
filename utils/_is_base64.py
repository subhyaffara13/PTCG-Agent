
def _is_base64(s):
    """Check if a string is valid base64."""
    import binascii

    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except binascii.Error:
        return False

