
def _check_nonce_length(
    nonce: utils.Buffer, name: str, algorithm: CipherAlgorithm
) -> None:
    if not isinstance(algorithm, BlockCipherAlgorithm):
        raise UnsupportedAlgorithm(
            f"{name} requires a block cipher algorithm",
            _Reasons.UNSUPPORTED_CIPHER,
        )
    if len(nonce) * 8 != algorithm.block_size:
        raise ValueError(f"Invalid nonce size ({len(nonce)}) for {name}.")

