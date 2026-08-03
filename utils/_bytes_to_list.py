import json

def _bytes_to_list(content: bytes) -> list:
    """Parse bytes from a Response object into a Python list.

    Expects the response body to be JSON-encoded data.

    NOTE: This is exactly the same implementation as `_bytes_to_dict` and will not complain if the returned data is a
    dictionary. The only advantage of having both is to help the user (and mypy) understand what kind of data to expect.
    """
    return json.loads(content.decode())

