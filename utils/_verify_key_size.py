
def _verify_key_size(
    algorithm: CipherAlgorithm, key: utils.Buffer
) -> utils.Buffer:
    # Verify that the key is instance of bytes
    utils._check_byteslike("key", key)

    # Verify that the key size matches the expected key size
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError(
            f"Invalid key size ({len(key) * 8}) for {algorithm.name}."
        )
    return key

