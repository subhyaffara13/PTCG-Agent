
def _canonicalize_fft_c2r_shape_and_dim_args(
    fname: str,
    input: TensorLikeType,
    s: ShapeType | None,
    dim: DimsType | None,
) -> _CanonicalizeC2rReturn:
    """Canonicalize shape and dim arguments for n-dimensional c2r transforms,
    as well as calculating the last_dim_size which is shape[dim[-1]] for the output"""
    (shape, dim) = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    torch._check(len(shape) > 0, lambda: f"{fname} must transform at least one axis")

    if s is None or s[-1] == -1:
        last_dim_size = 2 * (input.shape[dim[-1]] - 1)
    else:
        last_dim_size = shape[-1]

    torch._check(
        last_dim_size >= 1,
        lambda: f"Invalid number of data points ({last_dim_size}) specified",
    )

    shape_list = list(shape)
    shape_list[-1] = last_dim_size // 2 + 1
    return _CanonicalizeC2rReturn(
        shape=tuple(shape_list), dim=dim, last_dim_size=last_dim_size
    )

