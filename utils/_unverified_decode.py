
def _unverified_decode(token):
    """Decodes a token and does no verification.

    Args:
        token (Union[str, bytes]): The encoded JWT.

    Returns:
        Tuple[Mapping, Mapping, str, str]: header, payload, signed_section, and
            signature.

    Raises:
        google.auth.exceptions.MalformedError: if there are an incorrect amount of segments in the token or segments of the wrong type.
    """
    token = _helpers.to_bytes(token)

    if token.count(b".") != 2:
        raise exceptions.MalformedError(
            "Wrong number of segments in token: {0}".format(token)
        )

    encoded_header, encoded_payload, signature = token.split(b".")
    signed_section = encoded_header + b"." + encoded_payload
    signature = _helpers.padded_urlsafe_b64decode(signature)

    # Parse segments
    header = _decode_jwt_segment(encoded_header)
    payload = _decode_jwt_segment(encoded_payload)

    if not isinstance(header, Mapping):
        raise exceptions.MalformedError(
            "Header segment should be a JSON object: {0}".format(encoded_header)
        )

    if not isinstance(payload, Mapping):
        raise exceptions.MalformedError(
            "Payload segment should be a JSON object: {0}".format(encoded_payload)
        )

    return header, payload, signed_section, signature

