
def _check_aes_key_length(self: Mode, algorithm: CipherAlgorithm) -> None:
    if algorithm.key_size > 256 and algorithm.name == "AES":
        raise ValueError(
            "Only 128, 192, and 256 bit keys are allowed for this AES mode"
        )

