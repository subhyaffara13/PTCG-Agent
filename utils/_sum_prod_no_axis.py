
def _sum_prod_no_axis(x: Array, dtype: DType | None) -> Array:
    """
    Implements `sum(..., axis=())` and `prod(..., axis=())`.
    
    Works around https://github.com/pytorch/pytorch/issues/29137
    """
    if dtype is not None:
        return x.clone() if dtype == x.dtype else x.to(dtype)

    # We can't upcast uint8 according to the spec because there is no
    # torch.uint64, so at least upcast to int64 which is what prod does
    # when axis=None.
    if x.dtype in (torch.uint8, torch.int8, torch.int16, torch.int32):
        return x.to(torch.int64)

    return x.clone()

