
def meta_bucketize_scalar(
    self: NumberType,
    boundaries: Tensor,
    *,
    out_int32: bool = False,
    right: bool = False,
):
    return boundaries.new_empty(
        (),
        dtype=torch.int32 if out_int32 else torch.int64,
    )

