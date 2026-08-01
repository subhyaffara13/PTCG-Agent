
def hfftn(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = None,
    norm: NormType = None,
) -> TensorLikeType:
    shape, dim, last_dim_size = _canonicalize_fft_c2r_shape_and_dim_args(
        "hfftn", input, s, dim
    )
    input = _maybe_promote_tensor_fft(input, require_complex=True)
    input = _resize_fft_input(input, dim, shape)

    tmp = prims.fft_c2c(input, dim=dim[:-1], forward=True) if len(dim) > 1 else input
    tmp = _apply_norm(tmp, norm, _prod(shape[:-1]), forward=True)
    tmp = prims.conj_physical(tmp)
    out = prims.fft_c2r(tmp, dim=dim[-1:], last_dim_size=last_dim_size)
    return _apply_norm(out, norm, last_dim_size, forward=True)


def hfftn(x, s=None, axes=None, norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the N-D FFT of Hermitian symmetric complex input, i.e., a
    signal with a real spectrum.

    This function computes the N-D discrete Fourier Transform for a
    Hermitian symmetric complex input over any number of axes in an
    M-D array by means of the Fast Fourier Transform (FFT). In other
    words, ``ihfftn(hfftn(x, s)) == x`` to within numerical accuracy. (``s``
    here is ``x.shape`` with ``s[-1] = x.shape[-1] * 2 - 1``, this is necessary
    for the same reason ``x.shape`` would be necessary for `irfft`.)

    Parameters
    ----------
    x : array_like
        Input array.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (``s[0]`` refers to axis 0, ``s[1]`` to axis 1, etc.). `s` is also the
        number of input points used along this axis, except for the last axis,
        where ``s[-1]//2+1`` points of the input are used.
        Along any axis, if the shape indicated by `s` is smaller than that of
        the input, the input is cropped. If it is larger, the input is padded
        with zeros. If `s` is not given, the shape of the input along the axes
        specified by axes is used. Except for the last axis which is taken to be
        ``2*(m-1)`` where ``m`` is the length of the input along that axis.
    axes : sequence of ints, optional
        Axes over which to compute the inverse FFT. If not given, the last
        `len(s)` axes are used, or all axes if `s` is also not specified.
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
    out : ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `x`,
        as explained in the parameters section above.
        The length of each transformed axis is as given by the corresponding
        element of `s`, or the length of the input in every axis except for the
        last one if `s` is not given.  In the final transformed axis the length
        of the output when `s` is not given is ``2*(m-1)`` where ``m`` is the
        length of the final transformed axis of the input.  To get an odd
        number of output points in the final axis, `s` must be specified.

    Raises
    ------
    ValueError
        If `s` and `axes` have different length.
    IndexError
        If an element of `axes` is larger than the number of axes of `x`.

    See Also
    --------
    ihfftn : The inverse N-D FFT with real spectrum. Inverse of `hfftn`.
    fft : The 1-D FFT, with definitions and conventions used.
    rfft : Forward FFT of real input.

    Notes
    -----
    For a 1-D signal ``x`` to have a real spectrum, it must satisfy
    the Hermitian property::

        x[i] == np.conj(x[-i]) for all i

    This generalizes into higher dimensions by reflecting over each axis in
    turn::

        x[i, j, k, ...] == np.conj(x[-i, -j, -k, ...]) for all i, j, k, ...

    This should not be confused with a Hermitian matrix, for which the
    transpose is its own conjugate::

        x[i, j] == np.conj(x[j, i]) for all i, j


    The default value of `s` assumes an even output length in the final
    transformation axis. When performing the final complex to real
    transformation, the Hermitian symmetry requires that the last imaginary
    component along that axis must be 0 and so it is ignored. To avoid losing
    information, the correct length of the real input *must* be given.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.ones((3, 2, 2))
    >>> scipy.fft.hfftn(x)
    array([[[12.,  0.],
            [ 0.,  0.]],
           [[ 0.,  0.],
            [ 0.,  0.]],
           [[ 0.,  0.],
            [ 0.,  0.]]])

    """
    return (Dispatchable(x, np.ndarray),)


def hfftn(x, s=None, axes=None, norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    xp = array_namespace(x)
    if is_numpy(xp):
        x = np.asarray(x)
        return _duccfft.hfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)
    if is_complex(x, xp):
        x = xp.conj(x)
    return irfftn(x, s, axes, _swap_direction(norm),
                  overwrite_x, workers, plan=plan)

