
def _linalg_slogdet(A: Tensor) -> tuple[Tensor, Tensor, Tensor, Tensor]:
    squareCheckInputs(A, "linalg.slogdet")
    checkFloatingOrComplex(A, "linalg.slogdet", False)
    shape = A.shape
    sign = A.new_empty(shape[:-2])
    logabsdet = A.new_empty(shape[:-2], dtype=toRealValueType(A.dtype))
    LU = torch.empty_strided(
        size=shape,
        stride=make_contiguous_strides_for(shape, False),
        dtype=A.dtype,
        device=A.device,
    )
    pivots = A.new_empty(shape[:-1], dtype=torch.int32)
    return sign, logabsdet, LU, pivots

