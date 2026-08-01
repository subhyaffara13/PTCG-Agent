
def _check_block_size(data: utils.Buffer, block_len: int) -> None:
    """Require data to be full blocks"""
    if not data or len(data) % block_len != 0:
        raise ValueError("Corrupt data: missing padding")

