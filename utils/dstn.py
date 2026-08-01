
def dstn(x, type=2, s=None, axes=None, norm=None, overwrite_x=False,
         workers=None, orthogonalize=None):
    """
    Return multidimensional Discrete Sine Transform along the specified axes.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DST (see Notes). Default type is 2.
    s : int or array_like of ints or None, optional
        The shape of the result.  If both `s` and `axes` (see below) are None,
        `s` is ``x.shape``; if `s` is None but `axes` is not None, then `s` is
        ``numpy.take(x.shape, axes, axis=0)``.
        If ``s[i] > x.shape[i]``, the ith dimension of the input is padded with zeros.
        If ``s[i] < x.shape[i]``, the ith dimension of the input is truncated to length
        ``s[i]``.
        If any element of `shape` is -1, the size of the corresponding dimension
        of `x` is used.
    axes : int or array_like of ints or None, optional
        Axes over which the DST is computed. If not given, the last ``len(s)``
        axes are used, or all axes if `s` is also not specified.
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see Notes). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``.
        See :func:`~scipy.fft.fft` for more details.
    orthogonalize : bool, optional
        Whether to use the orthogonalized DST variant (see Notes).
        Defaults to ``True`` when ``norm="ortho"`` and ``False`` otherwise.

        .. versionadded:: 1.8.0

    Returns
    -------
    y : ndarray of real
        The transformed input array.

    See Also
    --------
    idstn : Inverse multidimensional DST

    Notes
    -----
    For full details of the DST types and normalization modes, as well as
    references, see `dst`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fft import dstn, idstn
    >>> rng = np.random.default_rng()
    >>> y = rng.standard_normal((16, 16))
    >>> np.allclose(y, idstn(dstn(y)))
    True

    """
    return (Dispatchable(x, np.ndarray),)


def dstn(x, type=2, s=None, axes=None, norm=None,
         overwrite_x=False, workers=None, orthogonalize=None):
    return _execute(_duccfft.dstn, x, type, s, axes, norm, 
                    overwrite_x, workers, orthogonalize)


def dstn(x, type=2, shape=None, axes=None, norm=None, overwrite_x=False):
    """
    Return multidimensional Discrete Sine Transform along the specified axes.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DST (see Notes). Default type is 2.
    shape : int or array_like of ints or None, optional
        The shape of the result.  If both `shape` and `axes` (see below) are
        None, `shape` is ``x.shape``; if `shape` is None but `axes` is
        not None, then `shape` is ``numpy.take(x.shape, axes, axis=0)``.
        If ``shape[i] > x.shape[i]``, the ith dimension is padded with zeros.
        If ``shape[i] < x.shape[i]``, the ith dimension is truncated to
        length ``shape[i]``.
        If any element of `shape` is -1, the size of the corresponding
        dimension of `x` is used.
    axes : int or array_like of ints or None, optional
        Axes along which the DCT is computed.
        The default is over all axes.
    norm : {None, 'ortho'}, optional
        Normalization mode (see Notes). Default is None.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    y : ndarray of real
        The transformed input array.

    See Also
    --------
    idstn : Inverse multidimensional DST

    Notes
    -----
    For full details of the DST types and normalization modes, as well as
    references, see `dst`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.fftpack import dstn, idstn
    >>> rng = np.random.default_rng()
    >>> y = rng.standard_normal((16, 16))
    >>> np.allclose(y, idstn(dstn(y, norm='ortho'), norm='ortho'))
    True

    """
    shape = _good_shape(x, shape, axes)
    return _duccfft.dstn(x, type, shape, axes, norm, overwrite_x)

