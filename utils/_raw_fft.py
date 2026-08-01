
def _raw_fft(a, n, axis, is_real, is_forward, norm, out=None):
    if n < 1:
        raise ValueError(f"Invalid number of FFT data points ({n}) specified.")

    # Calculate the normalization factor, passing in the array dtype to
    # avoid precision loss in the possible sqrt or reciprocal.
    if not is_forward:
        norm = _swap_direction(norm)

    real_dtype = result_type(a.real.dtype, 1.0)
    if norm is None or norm == "backward":
        fct = 1
    elif norm == "ortho":
        fct = reciprocal(sqrt(n, dtype=real_dtype))
    elif norm == "forward":
        fct = reciprocal(n, dtype=real_dtype)
    else:
        raise ValueError(f'Invalid norm value {norm}; should be "backward",'
                         '"ortho" or "forward".')

    n_out = n
    if is_real:
        if is_forward:
            ufunc = pfu.rfft_n_even if n % 2 == 0 else pfu.rfft_n_odd
            n_out = n // 2 + 1
        else:
            ufunc = pfu.irfft
    else:
        ufunc = pfu.fft if is_forward else pfu.ifft

    axis = normalize_axis_index(axis, a.ndim)

    if out is None:
        if is_real and not is_forward:  # irfft, complex in, real output.
            out_dtype = real_dtype
        else:  # Others, complex output.
            out_dtype = result_type(a.dtype, 1j)
        out = empty_like(a, shape=a.shape[:axis] + (n_out,) + a.shape[axis + 1:],
                         dtype=out_dtype)
    elif ((shape := getattr(out, "shape", None)) is not None
          and (len(shape) != a.ndim or shape[axis] != n_out)):
        raise ValueError("output array has wrong shape.")

    return ufunc(a, fct, axes=[(axis,), (), (axis,)], out=out)

