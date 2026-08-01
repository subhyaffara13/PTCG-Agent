
def _fft_c2c(
    func_name: str,
    input: TensorLikeType,
    n: int | None,
    dim: int,
    norm: NormType,
    forward: bool,
) -> TensorLikeType:
    """Common code for performing any complex to complex FFT (fft or ifft)"""
    torch._check(
        input.dtype.is_complex,
        lambda: f"{func_name} expects a complex input tensor, but got {input.dtype}",
    )
    dims = (utils.canonicalize_dim(input.ndim, dim, wrap_scalar=False),)
    dim_size = n if n is not None else input.shape[dim]
    torch._check(
        dim_size >= 1, lambda: f"Invalid number of data points ({dim_size}) specified"
    )

    if n is not None:
        input = _resize_fft_input(input, dims, (n,))

    ret = prims.fft_c2c(input, dim=dims, forward=forward)
    return _apply_norm(ret, norm, dim_size, forward)

