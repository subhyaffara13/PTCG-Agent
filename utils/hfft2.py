
def hfft2(
    input: TensorLikeType,
    s: ShapeType | None = None,
    dim: DimsType | None = (-2, -1),
    norm: NormType = None,
) -> TensorLikeType:
    return torch.fft.hfftn(input, s=s, dim=dim, norm=norm)


def hfft2(x, s=None, axes=(-2, -1), norm=None, overwrite_x=False, workers=None, *,
          plan=None):
    """
    Compute the 2-D FFT of a Hermitian complex array.

    Parameters
    ----------
    x : array
        Input array, taken to be Hermitian complex.
    s : sequence of ints, optional
        Shape of the real output.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see `fft`). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
        See `fft` for more details.
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
        The real result of the 2-D Hermitian complex real FFT.

    See Also
    --------
    hfftn : Compute the N-D discrete Fourier Transform for Hermitian
            complex input.

    Notes
    -----
    This is really just `hfftn` with different default behavior.
    For more details see `hfftn`.

    Examples
    --------
    >>> import scipy.fft
    >>> import numpy as np
    >>> x = np.array([[1+0j, 2+0j], [2+0j, 1+0j]])  # Hermitian-symmetric input
    >>> scipy.fft.hfft2(x, s=(2, 2))
    array([[ 6.,  0.],
           [ 0., -2.]])

    """
    return (Dispatchable(x, np.ndarray),)


def hfft2(x, s=None, axes=(-2, -1), norm=None,
          overwrite_x=False, workers=None, *, plan=None):
    return hfftn(x, s, axes, norm, overwrite_x, workers, plan=plan)


def hfft2(x, s=None, axes=(-2,-1), norm=None, overwrite_x=False, workers=None,
          *, plan=None):
    """
    2-D discrete Fourier transform of a Hermitian sequence
    """
    if plan is not None:
        raise NotImplementedError('Passing a precomputed plan is not yet '
                                  'supported by scipy.fft functions')
    return hfftn(x, s, axes, norm, overwrite_x, workers)

