
def _verify_rsa_parameters(public_exponent: int, key_size: int) -> None:
    if public_exponent not in (3, 65537):
        raise ValueError(
            "public_exponent must be either 3 (for legacy compatibility) or "
            "65537. Almost everyone should choose 65537 here!"
        )

    if key_size < 1024:
        raise ValueError("key_size must be at least 1024-bits.")

