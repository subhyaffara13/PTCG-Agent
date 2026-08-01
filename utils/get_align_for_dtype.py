
def get_align_for_dtype(dtype: torch.dtype) -> int:
    return config.padding_alignment_bytes // dtype.itemsize

