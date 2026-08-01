
def _wrap_core(
    wrapping_key: bytes,
    a: bytes,
    r: list[bytes],
) -> bytes:
    # RFC 3394 Key Wrap - 2.2.1 (index method)
    encryptor = Cipher(AES(wrapping_key), ECB()).encryptor()
    n = len(r)
    for j in range(6):
        for i in range(n):
            # every encryption operation is a discrete 16 byte chunk (because
            # AES has a 128-bit block size) and since we're using ECB it is
            # safe to reuse the encryptor for the entire operation
            b = encryptor.update(a + r[i])
            a = (
                int.from_bytes(b[:8], byteorder="big") ^ ((n * j) + i + 1)
            ).to_bytes(length=8, byteorder="big")
            r[i] = b[-8:]

    assert encryptor.finalize() == b""

    return a + b"".join(r)

