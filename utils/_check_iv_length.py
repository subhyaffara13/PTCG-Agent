
def _check_iv_length(
    self: ModeWithInitializationVector, algorithm: BlockCipherAlgorithm
) -> None:
    iv_len = len(self.initialization_vector)
    if iv_len * 8 != algorithm.block_size:
        raise ValueError(f"Invalid IV size ({iv_len}) for {self.name}.")

