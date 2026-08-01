
def _tensor_nbytes(numel: int, dtype: torch.dtype) -> int:
    return numel * dtype.itemsize

