
def _check_iv_and_key_length(
    self: ModeWithInitializationVector, algorithm: CipherAlgorithm
) -> None:
    if not isinstance(algorithm, BlockCipherAlgorithm):
        raise UnsupportedAlgorithm(
            f"{self} requires a block cipher algorithm",
            _Reasons.UNSUPPORTED_CIPHER,
        )
    _check_aes_key_length(self, algorithm)
    _check_iv_length(self, algorithm)

