
def _int_to_base64url(n: int) -> str:
    """Encode an integer as a base64url string (no padding)."""
    byte_length = (n.bit_length() + 7) // 8
    return (
        base64.urlsafe_b64encode(n.to_bytes(byte_length, byteorder="big"))
        .rstrip(b"=")
        .decode("ascii")
    )

