
def aes_key_unwrap_with_padding(
    wrapping_key: bytes,
    wrapped_key: bytes,
    backend: typing.Any = None,
) -> bytes:
    if len(wrapped_key) < 16:
        raise InvalidUnwrap("Must be at least 16 bytes")

    if len(wrapping_key) not in [16, 24, 32]:
        raise ValueError("The wrapping key must be a valid AES key length")

    if len(wrapped_key) == 16:
        # RFC 5649 - 4.2 - exactly two 64-bit blocks
        decryptor = Cipher(AES(wrapping_key), ECB()).decryptor()
        out = decryptor.update(wrapped_key)
        assert decryptor.finalize() == b""
        a = out[:8]
        data = out[8:]
        n = 1
    else:
        r = [wrapped_key[i : i + 8] for i in range(0, len(wrapped_key), 8)]
        encrypted_aiv = r.pop(0)
        n = len(r)
        a, r = _unwrap_core(wrapping_key, encrypted_aiv, r)
        data = b"".join(r)

    # 1) Check that MSB(32,A) = A65959A6.
    # 2) Check that 8*(n-1) < LSB(32,A) <= 8*n.  If so, let
    #    MLI = LSB(32,A).
    # 3) Let b = (8*n)-MLI, and then check that the rightmost b octets of
    #    the output data are zero.
    mli = int.from_bytes(a[4:], byteorder="big")
    b = (8 * n) - mli
    if (
        not bytes_eq(a[:4], b"\xa6\x59\x59\xa6")
        or not 8 * (n - 1) < mli <= 8 * n
        or (b != 0 and not bytes_eq(data[-b:], b"\x00" * b))
    ):
        raise InvalidUnwrap()

    if b == 0:
        return data
    else:
        return data[:-b]

