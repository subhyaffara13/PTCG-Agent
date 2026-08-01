
def _fftconv_faster(x, h, mode):
    """
    See if using fftconvolve or convolve is faster.

    Parameters
    ----------
    x : np.ndarray
        Signal
    h : np.ndarray
        Kernel
    mode : str
        Mode passed to convolve

    Returns
    -------
    fft_faster : bool

    Notes
    -----
    See docstring of `choose_conv_method` for details on tuning hardware.

    See pull request 11031 for more detail:
    https://github.com/scipy/scipy/pull/11031.

    """
    fft_ops, direct_ops = _conv_ops(x.shape, h.shape, mode)
    offset = -1e-3 if x.ndim == 1 else -1e-4
    constants = {
            "valid": (1.89095737e-9, 2.1364985e-10, offset),
            "full": (1.7649070e-9, 2.1414831e-10, offset),
            "same": (3.2646654e-9, 2.8478277e-10, offset)
            if h.size <= x.size
            else (3.21635404e-9, 1.1773253e-8, -1e-5),
    } if x.ndim == 1 else {
            "valid": (1.85927e-9, 2.11242e-8, offset),
            "full": (1.99817e-9, 1.66174e-8, offset),
            "same": (2.04735e-9, 1.55367e-8, offset),
    }
    O_fft, O_direct, O_offset = constants[mode]
    return O_fft * fft_ops < O_direct * direct_ops + O_offset

