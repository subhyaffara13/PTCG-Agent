
def aes_key_wrap_with_padding(
    wrapping_key: bytes,
    key_to_wrap: bytes,
    backend: typing.Any = None,
) -> bytes:
    if len(wrapping_key) not in [16, 24, 32]:
        raise ValueError("The wrapping key must be a valid AES key length")

    if not key_to_wrap or len(key_to_wrap) > 2**32:
        raise ValueError("key_to_wrap must be between 1 and 2^32 bytes")

    aiv = b"\xa6\x59\x59\xa6" + len(key_to_wrap).to_bytes(
        length=4, byteorder="big"
    )
    # pad the key to wrap if necessary
    pad = (8 - (len(key_to_wrap) % 8)) % 8
    key_to_wrap = key_to_wrap + b"\x00" * pad
    if len(key_to_wrap) == 8:
        # RFC 5649 - 4.1 - exactly 8 octets after padding
        encryptor = Cipher(AES(wrapping_key), ECB()).encryptor()
        b = encryptor.update(aiv + key_to_wrap)
        assert encryptor.finalize() == b""
        return b
    else:
        r = [key_to_wrap[i : i + 8] for i in range(0, len(key_to_wrap), 8)]
        return _wrap_core(wrapping_key, aiv, r)

