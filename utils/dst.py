
def dst(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False, workers=None,
        orthogonalize=None):
    r"""
    Return the Discrete Sine Transform of arbitrary type sequence x.

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
        Axis along which the dst is computed; the default is over the
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
        Whether to use the orthogonalized DST variant (see Notes).
        Defaults to ``True`` when ``norm="ortho"`` and ``False`` otherwise.

        .. versionadded:: 1.8.0

    Returns
    -------
    dst : ndarray of reals
        The transformed input array.

    See Also
    --------
    idst : Inverse DST

    Notes
    -----
    .. warning:: For ``type in {2, 3}``, ``norm="ortho"`` breaks the direct
                 correspondence with the direct Fourier transform. To recover
                 it you must specify ``orthogonalize=False``.

    For ``norm="ortho"`` both the `dst` and `idst` are scaled by the same
    overall factor in both directions. By default, the transform is also
    orthogonalized which for types 2 and 3 means the transform definition is
    modified to give orthogonality of the DST matrix (see below).

    For ``norm="backward"``, there is no scaling on the `dst` and the `idst` is
    scaled by ``1/N`` where ``N`` is the "logical" size of the DST.

    There are, theoretically, 8 types of the DST for different combinations of
    even/odd boundary conditions and boundary off sets [1]_, only the first
    4 types are implemented in SciPy.

    **Type I**

    There are several definitions of the DST-I; we use the following for
    ``norm="backward"``. DST-I assumes the input is odd around :math:`n=-1` and
    :math:`n=N`.

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(k+1)(n+1)}{N+1}\right)

    Note that the DST-I is only supported for input size > 1.
    The (unnormalized) DST-I is its own inverse, up to a factor :math:`2(N+1)`.
    The orthonormalized DST-I is exactly its own inverse.

    ``orthogonalize`` has no effect here, as the DST-I matrix is already
    orthogonal up to a scale factor of ``2N``.

    **Type II**

    There are several definitions of the DST-II; we use the following for
    ``norm="backward"``. DST-II assumes the input is odd around :math:`n=-1/2` and
    :math:`n=N-1/2`; the output is odd around :math:`k=-1` and even around :math:`k=N-1`

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(k+1)(2n+1)}{2N}\right)

    If ``orthogonalize=True``, ``y[-1]`` is divided :math:`\sqrt{2}` which, when
    combined with ``norm="ortho"``, makes the corresponding matrix of
    coefficients orthonormal (``O @ O.T = np.eye(N)``).

    **Type III**

    There are several definitions of the DST-III, we use the following (for
    ``norm="backward"``). DST-III assumes the input is odd around :math:`n=-1` and
    even around :math:`n=N-1`

    .. math::

        y_k = (-1)^k x_{N-1} + 2 \sum_{n=0}^{N-2} x_n \sin\left(
        \frac{\pi(2k+1)(n+1)}{2N}\right)

    If ``orthogonalize=True``, ``x[-1]`` is multiplied by :math:`\sqrt{2}`
    which, when combined with ``norm="ortho"``, makes the corresponding matrix
    of coefficients orthonormal (``O @ O.T = np.eye(N)``).

    The (unnormalized) DST-III is the inverse of the (unnormalized) DST-II, up
    to a factor :math:`2N`. The orthonormalized DST-III is exactly the inverse of the
    orthonormalized DST-II.

    **Type IV**

    There are several definitions of the DST-IV, we use the following (for
    ``norm="backward"``). DST-IV assumes the input is odd around :math:`n=-1/2` and
    even around :math:`n=N-1/2`

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(2k+1)(2n+1)}{4N}\right)

    ``orthogonalize`` has no effect here, as the DST-IV matrix is already
    orthogonal up to a scale factor of ``2N``.

    The (unnormalized) DST-IV is its own inverse, up to a factor :math:`2N`. The
    orthonormalized DST-IV is exactly its own inverse.

    Examples
    --------
    Compute the DST of a simple 1D array:

    >>> import numpy as np
    >>> from scipy.fft import dst
    >>> x = np.array([1, -1, 1, -1])
    >>> dst(x, type=2)
    array([0., 0., 0., 8.])

    This computes the Discrete Sine Transform (DST) of type-II for the input array.
    The output contains the transformed values corresponding to the given input sequence

    References
    ----------
    .. [1] Wikipedia, "Discrete sine transform",
           https://en.wikipedia.org/wiki/Discrete_sine_transform

    """
    return (Dispatchable(x, np.ndarray),)


def dst(x, type=2, n=None, axis=-1, norm=None,
        overwrite_x=False, workers=None, orthogonalize=None):
    return _execute(_duccfft.dst, x, type, n, axis, norm, 
                    overwrite_x, workers, orthogonalize)


def dst(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False):
    r"""
    Return the Discrete Sine Transform of arbitrary type sequence x.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DST (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the dst is computed; the default is over the
        last axis (i.e., ``axis=-1``).
    norm : {None, 'ortho'}, optional
        Normalization mode (see Notes). Default is None.
    overwrite_x : bool, optional
        If True, the contents of `x` can be destroyed; the default is False.

    Returns
    -------
    dst : ndarray of reals
        The transformed input array.

    See Also
    --------
    idst : Inverse DST

    Notes
    -----
    For a single dimension array ``x``.

    There are, theoretically, 8 types of the DST for different combinations of
    even/odd boundary conditions and boundary off sets [1]_, only the first
    4 types are implemented in scipy.

    **Type I**

    There are several definitions of the DST-I; we use the following
    for ``norm=None``. DST-I assumes the input is odd around `n=-1` and `n=N`.

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(k+1)(n+1)}{N+1}\right)

    Note that the DST-I is only supported for input size > 1.
    The (unnormalized) DST-I is its own inverse, up to a factor ``2(N+1)``.
    The orthonormalized DST-I is exactly its own inverse.

    **Type II**

    There are several definitions of the DST-II; we use the following for
    ``norm=None``. DST-II assumes the input is odd around `n=-1/2` and
    `n=N-1/2`; the output is odd around :math:`k=-1` and even around `k=N-1`

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(k+1)(2n+1)}{2N}\right)

    if ``norm='ortho'``, ``y[k]`` is multiplied by a scaling factor ``f``

    .. math::

        f = \begin{cases}
        \sqrt{\frac{1}{4N}} & \text{if }k = 0, \\
        \sqrt{\frac{1}{2N}} & \text{otherwise} \end{cases}

    **Type III**

    There are several definitions of the DST-III, we use the following (for
    ``norm=None``). DST-III assumes the input is odd around `n=-1` and even
    around `n=N-1`

    .. math::

        y_k = (-1)^k x_{N-1} + 2 \sum_{n=0}^{N-2} x_n \sin\left(
        \frac{\pi(2k+1)(n+1)}{2N}\right)

    The (unnormalized) DST-III is the inverse of the (unnormalized) DST-II, up
    to a factor ``2N``. The orthonormalized DST-III is exactly the inverse of the
    orthonormalized DST-II.

    .. versionadded:: 0.11.0

    **Type IV**

    There are several definitions of the DST-IV, we use the following (for
    ``norm=None``). DST-IV assumes the input is odd around `n=-0.5` and even
    around `n=N-0.5`

    .. math::

        y_k = 2 \sum_{n=0}^{N-1} x_n \sin\left(\frac{\pi(2k+1)(2n+1)}{4N}\right)

    The (unnormalized) DST-IV is its own inverse, up to a factor ``2N``. The
    orthonormalized DST-IV is exactly its own inverse.

    .. versionadded:: 1.2.0
       Support for DST-IV.

    References
    ----------
    .. [1] Wikipedia, "Discrete sine transform",
           https://en.wikipedia.org/wiki/Discrete_sine_transform

    """
    return _duccfft.dst(x, type, n, axis, norm, overwrite_x)

