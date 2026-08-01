
def _init_cipher(
    ciphername: bytes,
    password: bytes | None,
    salt: bytes,
    rounds: int,
) -> Cipher[modes.CBC | modes.CTR | modes.GCM]:
    """Generate key + iv and return cipher."""
    if not password:
        raise TypeError(
            "Key is password-protected, but password was not provided."
        )

    ciph = _SSH_CIPHERS[ciphername]
    seed = _bcrypt_kdf(
        password, salt, ciph.key_len + ciph.iv_len, rounds, True
    )
    return Cipher(
        ciph.alg(seed[: ciph.key_len]),
        ciph.mode(seed[ciph.key_len :]),
    )

