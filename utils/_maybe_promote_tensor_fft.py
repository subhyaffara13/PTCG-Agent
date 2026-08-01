
def _maybe_promote_tensor_fft(
    t: TensorLikeType, require_complex: bool = False
) -> TensorLikeType:
    """Helper to promote a tensor to a dtype supported by the FFT primitives"""
    cur_type = t.dtype
    new_type = _promote_type_fft(cur_type, require_complex, t.device)
    return _maybe_convert_to_dtype(t, new_type)  # type: ignore[return-value]

