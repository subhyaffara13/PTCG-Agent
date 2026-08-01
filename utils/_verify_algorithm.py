
def _verify_algorithm(algorithm: hashes.HashAlgorithm) -> None:
    if not isinstance(algorithm, _ALLOWED_HASHES):
        raise ValueError(
            "Algorithm must be SHA1, SHA224, SHA256, SHA384, or SHA512"
        )

