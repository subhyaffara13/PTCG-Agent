
def ihfft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.ihfftn(input, s=s, dim=dim, norm=norm)


def ihfft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
           plan=None):
    """
    Compute the 2-D inverse FFT of a real spectrum.

    Parameters
    ----------
    x : array_like
        The input array
    s : sequence of ints, optional
        Shape of the real input to the inverse FFT.
    axes : sequence of ints, optional
        The axes over which to compute the inverse fft.
        Default is the last two axes.
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
        The result of the inverse real 2-D FFT.

    See Also
    --------
    ihfftn : Compute the inverse of the N-D FFT of Hermitian input.

    Notes
    -----
    This is really `ihfftn` with different defaults.
    For more details see `ihfftn`.

    """
    return (Dispatchable(x, np.ndarray),)


def ihfft2(x, s=None, axes=(-2, -1), norm=None,
           overwrite_x=False, workers=None, *, plan=None):
    return ihfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def ihfft2(x, s=None, axes=(-2,-1), norm=None, overwrite_x=False, workers=None,
           *, plan=None):
    """
    2-D discrete inverse Fourier transform of a Hermitian sequence
    """
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    return ihfftn(x, s, axes, norm, overwrite_x, workers)

