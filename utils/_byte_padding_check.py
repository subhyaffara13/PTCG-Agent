
def _byte_padding_check(block_size: int) -> None:
    if not (0 <= block_size <= 2040):
        raise ValueError("block_size must be in range(0, 2041).")

    if block_size % 8 != 0:
        raise ValueError("block_size must be a multiple of 8.")

