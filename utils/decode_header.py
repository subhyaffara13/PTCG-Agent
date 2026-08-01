
def decode_header(token):
    """Return the decoded header of a token.

    No verification is done. This is useful to extract the key id from
    the header in order to acquire the appropriate certificate to verify
    the token.

    Args:
        token (Union[str, bytes]): the encoded JWT.

    Returns:
        Mapping: The decoded JWT header.
    """
    header, _, _, _ = _unverified_decode(token)
    return header

