
def _unwrap_core(
    wrapping_key: bytes,
    a: bytes,
    r: list[bytes],
) -> tuple[bytes, list[bytes]]:
    # Implement RFC 3394 Key Unwrap - 2.2.2 (index method)
    decryptor = Cipher(AES(wrapping_key), ECB()).decryptor()
    n = len(r)
    for j in reversed(range(6)):
        for i in reversed(range(n)):
            atr = (
                int.from_bytes(a, byteorder="big") ^ ((n * j) + i + 1)
            ).to_bytes(length=8, byteorder="big") + r[i]
            # every decryption operation is a discrete 16 byte chunk so
            # it is safe to reuse the decryptor for the entire operation
            b = decryptor.update(atr)
            a = b[:8]
            r[i] = b[-8:]

    assert decryptor.finalize() == b""
    return a, r

