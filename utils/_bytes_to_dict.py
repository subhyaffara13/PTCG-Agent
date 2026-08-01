
def _bytes_to_dict(content: bytes) -> dict:
    """Parse bytes from a Response object into a Python dictionary.

    Expects the response body to be JSON-encoded data.

    NOTE: This is exactly the same implementation as `_bytes_to_list` and will not complain if the returned data is a
    list. The only advantage of having both is to help the user (and mypy) understand what kind of data to expect.
    """
    return json.loads(content.decode())

