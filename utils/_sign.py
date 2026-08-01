
def _sign(x):
    return int(copysign(1, x))


def _sign(n):
    if n < 0:
        return -1, -n
    return 1, n


def _sign(key, msg):
    """Creates the HMAC-SHA256 hash of the provided message using the provided
    key.

    Args:
        key (str): The HMAC-SHA256 key to use.
        msg (str): The message to hash.

    Returns:
        str: The computed hash bytes.
    """
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

