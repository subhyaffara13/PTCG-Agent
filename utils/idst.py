
def idst(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False,
         workers=None, orthogonalize=None):
    """
    Return the Inverse Discrete Sine Transform of an arbitrary type sequence.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DST (see Notes). Default type is 2.
    n : int, optional
        Length of the transform. If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the idst is computed; the default is over the
        last axis (i.e., ``axis=-1``).
    norm : {"backward", "ortho", "forward"}, optional
        Normalization mode (see Notes). Default is "backward".
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.
    workers : int, optional
        Maximum number of workers to use for parallel computation. If negative,
        the value wraps around from ``os.cpu_count()``.
        See :func:`~scipy.fft.fft` for more details.
    orthogonalize : bool, optional
        Whether to use the orthogonalized IDST variant (see Notes).
        Defaults to ``True`` when ``norm="ortho"`` and ``False`` otherwise.

        .. versionadded:: 1.8.0

    Returns
    -------
    idst : ndarray of real
        The transformed input array.

    See Also
    --------
    dst : Forward DST
    irfft : Inverse FFT for real input

    Notes
    -----
    .. warning:: For ``type in {2, 3}``, ``norm="ortho"`` breaks the direct
                 correspondence with the inverse direct Fourier transform.

    For ``norm="ortho"`` both the `dst` and `idst` are scaled by the same
    overall factor in both directions. By default, the transform is also
    orthogonalized which for types 2 and 3 means the transform definition is
    modified to give orthogonality of the DST matrix (see `dst` for the full
    definitions).

    'The' IDST is the IDST-II, which is the same as the normalized DST-III.

    The IDST is equivalent to a normal DST except for the normalization and
    type. DST type 1 and 4 are their own inverse and DSTs 2 and 3 are each
    other's inverses. For an example that demonstrates the relation between
    the DST and ISDT, consult the :ref:`DST and IDST <tutorial_FFT_DST_and_IDST>`
    section of the :ref:`user_guide`.

    Examples
    --------
    The following example calculates the signal from a spectrum `X` where only the first
    bin has a non-zero value. The signal for all four DST types is plotted:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.fft import idst
    ...
    >>> N = 15
    >>> X = np.array([0, N])  # the last `N-2` bin zero-valued bins are not needed
    ...
    >>> _, ax = plt.subplots()
    >>> ax.set(title=f"Inverse of one component DST ({N} samples)",
    ...        xlim=(0, N), xlabel="k", ylabel="x[k]")
    >>> for t_ in range(1, 5):
    ...     x = idst(X, type=t_, n=N)  # parameter `n` pads `X` to length `N`.
    ...     ax.plot(x, '.-', alpha=0.5, label=f"Type {t_}")
    >>> ax.grid(True)
    >>> ax.legend()
    >>> plt.show()

    The resulting signals are sines with their period and their phase determined by the
    used DST type. The following table shows those, with `N` being the number of signal
    samples and `n` is the index of the non-zero bin (here: ``N, n = 15, 1``):

    +------+------------------------------+------------------------+
    | Type | period in samples            | phase shift in samples |
    +======+==============================+========================+
    |  1   | :math:`2 (N+1) / (n+1) = 16` | :math:`-1`             |
    +------+------------------------------+------------------------+
    |  2   | :math:`2 N / (n+1) = 15`     | :math:`-1/2`           |
    +------+------------------------------+------------------------+
    |  3   | :math:`2 N / (n+1/2) = 20`   | :math:`-1`             |
    +------+------------------------------+------------------------+
    |  4   | :math:`2 N / (n+1/2) = 20`   | :math:`-1/2`           |
    +------+------------------------------+------------------------+

    """
    return (Dispatchable(x, np.ndarray),)


def idst(x, type=2, n=None, axis=-1, norm=None,
         overwrite_x=False, workers=None, orthogonalize=None):
    return _execute(_duccfft.idst, x, type, n, axis, norm, 
                    overwrite_x, workers, orthogonalize)


def idst(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False):
    """
    Return the Inverse Discrete Sine Transform of an arbitrary type sequence.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DST (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated. If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the idst is computed; the default is over the
        last axis (i.e., ``axis=-1``).
    norm : {None, 'ortho'}, optional
        Normalization mode (see Notes). Default is None.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    idst : ndarray of real
        The transformed input array.

    See Also
    --------
    dst : Forward DST

    Notes
    -----
    'The' IDST is the IDST of type 2, which is the same as DST of type 3.

    IDST of type 1 is the DST of type 1, IDST of type 2 is the DST of type
    3, and IDST of type 3 is the DST of type 2. For the definition of these
    types, see `dst`.

    .. versionadded:: 0.11.0

    """
    type = _inverse_typemap[type]
    return _duccfft.dst(x, type, n, axis, norm, overwrite_x)

