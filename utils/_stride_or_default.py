
def _stride_or_default(
    stride: torch._prims_common.StrideType | None,
    *,
    shape: torch._prims_common.ShapeType,
) -> torch._prims_common.StrideType:
    return stride if stride is not None else utils.make_contiguous_strides_for(shape)

