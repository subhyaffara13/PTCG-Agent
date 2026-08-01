
def ihfftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    torch._check(
        not input.dtype.is_complex,
        lambda: f"ihfftn expects a real-valued input tensor, but got {input.dtype}",
    )
    shape, dim = _canonicalize_fft_shape_and_dim_args(input, s, dim)
    torch._check(len(shape) > 0, lambda: "ihfftn must transform at least one axis")
    input = _maybe_promote_tensor_fft(input, require_complex=False)
    input = _resize_fft_input(input, dim, shape)

    tmp = prims.fft_r2c(input, dim=dim[-1:], onesided=True)

    if len(dim) == 1:
        tmp = _apply_norm(tmp, norm=norm, signal_numel=shape[0], forward=False)
        return prims.conj(tmp)

    tmp = prims.conj_physical(tmp)
    tmp = prims.fft_c2c(tmp, dim=dim[:-1], forward=False)
    return _apply_norm(tmp, norm=norm, signal_numel=_prod(shape), forward=False)


def ihfftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
           plan=None):
    """
    Compute the N-D inverse discrete Fourier Transform for a real
    spectrum.

    This function computes the N-D inverse discrete Fourier Transform
    over any number of axes in an M-D real array by means of the Fast
    Fourier Transform (FFT). By default, all axes are transformed, with the
    real transform performed over the last axis, while the remaining transforms
    are complex.

    Parameters
    ----------
    x : array_like
        Input array, taken to be real.
    s : sequence of ints, optional
        Shape (length along each transformed axis) to use from the input.
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.).
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped. If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input along the axes specified
        by `axes` is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT. If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `fft`). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
        See :func:`fft` for more details.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``.
        See :func:`~scipy.fft.fft` for more details.
    plan : object, optional
        This argument is reserved for passing in a precomputed plan provided
        by downstream FFT vendors. It is currently not used in SciPy.

        .. versionadded:: 1.5.0

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` and `x`,
        as explained in the parameters section above.
        The length of the last axis transformed will be ``s[-1]//2+1``,
        while the remaining transformed axes will have lengths according to
        `s`, or unchanged from the input.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    hfftn : The forward N-D FFT of Hermitian input.
    hfft : The 1-D FFT of Hermitian input.
    fft : The 1-D FFT, with definitions and conventions used.
    fftn : The N-D FFT.
    hfft2 : The 2-D FFT of Hermitian input.

    Notes
    -----
    The transform for real input is performed over the last transformation
    axis, as by `ihfft`, then the transform over the remaining axes is
    performed as by `ifftn`. The order of the output is the positive part of
    the Hermitian output signal, in the same format as `rfft`.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.ones((2, 2, 2))
    >>> scipy.fft.ihfftn(x)
    array([[[1.+0.j,  0.+0.j], # may vary
            [0.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])
    >>> scipy.fft.ihfftn(x, axes=(2, 0))
    array([[[1.+0.j,  0.+0.j], # may vary
            [1.+0.j,  0.+0.j]],
           [[0.+0.j,  0.+0.j],
            [0.+0.j,  0.+0.j]]])

    """
    return (Dispatchable(x, np.ndarray),)


def ihfftn(x, s=None, axes=None, norm=None,
           overwrite_x=False, workers=None, *, plan=None):
    xp = array_namespace(x)
    if is_numpy(xp):
        x = np.asarray(x)
        return _duccfft.ihfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)
    return xp.conj(rfftn(x, s, axes, _swap_direction(norm),
                         overwrite_x, workers, plan=plan))

