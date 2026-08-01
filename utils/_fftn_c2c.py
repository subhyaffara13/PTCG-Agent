
def _fftn_c2c(
    function_name: str,
    input: TensorLikeType,
    shape: tuple[int, ...],
    dim: tuple[int, ...],
    norm: NormType,
    forward: bool,
) -> TensorLikeType:
    """Common code for n-dimensional complex to complex FFTs (fftn or ifftn)"""
    torch._check(
        input.dtype.is_complex,
        lambda: f"{function_name} expects a complex input tensor, "
        f"but got {input.dtype}",
    )
    x = _resize_fft_input(input, dim, shape)
    output = prims.fft_c2c(x, dim=dim, forward=forward)
    return _apply_norm(output, norm=norm, signal_numel=_prod(shape), forward=forward)

