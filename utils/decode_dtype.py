
def decode_dtype(dtype: int | torch.dtype) -> torch.dtype:
    if not isinstance(dtype, int):
        return dtype
    assert dtype in DTYPE_ID_LOOKUP, f"id {dtype} missing from DTYPE_ID_LOOKUP"

    dtype = DTYPE_ID_LOOKUP[dtype]
    return dtype

