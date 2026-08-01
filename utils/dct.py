
def dct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False, workers=None,
        orthogonalize=None):
    r"""Return the Discrete Cosine Transform of arbitrary type sequence x.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the dct is computed; the default is over the
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
        Whether to use the orthogonalized DCT variant (see Notes).
        Defaults to ``True`` when ``norm="ortho"`` and ``False`` otherwise.

        .. versionadded:: 1.8.0

    Returns
    -------
    y : ndarray of real
        The transformed input array.

    See Also
    --------
    idct : Inverse DCT

    Notes
    -----
    For a single dimension array ``x``, ``dct(x, norm='ortho')`` is equal to
    MATLAB ``dct(x)``.

    .. warning:: For ``type in {1, 2, 3}``, ``norm="ortho"`` breaks the direct
                 correspondence with the direct Fourier transform. To recover
                 it you must specify ``orthogonalize=False``.

    For ``norm="ortho"`` both the `dct` and `idct` are scaled by the same
    overall factor in both directions. By default, the transform is also
    orthogonalized which for types 1, 2 and 3 means the transform definition is
    modified to give orthogonality of the DCT matrix (see below).

    For ``norm="backward"``, there is no scaling on `dct` and the `idct` is
    scaled by ``1/N`` where ``N`` is the "logical" size of the DCT. For
    ``norm="forward"`` the ``1/N`` normalization is applied to the forward
    `dct` instead and the `idct` is unnormalized.

    There are, theoretically, 8 types of the DCT, only the first 4 types are
    implemented in SciPy.'The' DCT generally refers to DCT type 2, and 'the'
    Inverse DCT generally refers to DCT type 3.

    **Type I**

    There are several definitions of the DCT-I; we use the following
    (for ``norm="backward"``)

    .. math::

       y_k = x_0 + (-1)^k x_{N-1} + 2 \sum_{n=1}^{N-2} x_n \cos\left(
       \frac{\pi k n}{N-1} \right)

    If ``orthogonalize=True``, ``x[0]`` and ``x[N-1]`` are multiplied by a
    scaling factor of :math:`\sqrt{2}`, and ``y[0]`` and ``y[N-1]`` are divided
    by :math:`\sqrt{2}`. When combined with ``norm="ortho"``, this makes the
    corresponding matrix of coefficients orthonormal (``O @ O.T = np.eye(N)``).

    .. note::
       The DCT-I is only supported for input size > 1.

    **Type II**

    There are several definitions of the DCT-II; we use the following
    (for ``norm="backward"``)

    .. math::

       y_k = 2 \sum_{n=0}^{N-1} x_n \cos\left(\frac{\pi k(2n+1)}{2N} \right)

    If ``orthogonalize=True``, ``y[0]`` is divided by :math:`\sqrt{2}` which,
    when combined with ``norm="ortho"``, makes the corresponding matrix of
    coefficients orthonormal (``O @ O.T = np.eye(N)``).

    **Type III**

    There are several definitions, we use the following (for
    ``norm="backward"``)

    .. math::

       y_k = x_0 + 2 \sum_{n=1}^{N-1} x_n \cos\left(\frac{\pi(2k+1)n}{2N}\right)

    If ``orthogonalize=True``, ``x[0]`` terms are multiplied by
    :math:`\sqrt{2}` which, when combined with ``norm="ortho"``, makes the
    corresponding matrix of coefficients orthonormal (``O @ O.T = np.eye(N)``).

    The (unnormalized) DCT-III is the inverse of the (unnormalized) DCT-II, up
    to a factor `2N`. The orthonormalized DCT-III is exactly the inverse of
    the orthonormalized DCT-II.

    **Type IV**

    There are several definitions of the DCT-IV; we use the following
    (for ``norm="backward"``)

    .. math::

       y_k = 2 \sum_{n=0}^{N-1} x_n \cos\left(\frac{\pi(2k+1)(2n+1)}{4N} \right)

    ``orthogonalize`` has no effect here, as the DCT-IV matrix is already
    orthogonal up to a scale factor of ``2N``.

    References
    ----------
    .. [1] 'A Fast Cosine Transform in One and Two Dimensions', by J.
           Makhoul, `IEEE Transactions on acoustics, speech and signal
           processing` vol. 28(1), pp. 27-34,
           :doi:`10.1109/TASSP.1980.1163351` (1980).
    .. [2] Wikipedia, "Discrete cosine transform",
           https://en.wikipedia.org/wiki/Discrete_cosine_transform

    Examples
    --------
    The Type 1 DCT is equivalent to the FFT (though faster) for real,
    even-symmetrical inputs. The output is also real and even-symmetrical.
    Half of the FFT input is used to generate half of the FFT output:

    >>> from scipy.fft import fft, dct
    >>> import numpy as np
    >>> fft(np.array([4., 3., 5., 10., 5., 3.])).real
    array([ 30.,  -8.,   6.,  -2.,   6.,  -8.])
    >>> dct(np.array([4., 3., 5., 10.]), 1)
    array([ 30.,  -8.,   6.,  -2.])

    """
    return (Dispatchable(x, np.ndarray),)


def dct(x, type=2, n=None, axis=-1, norm=None,
        overwrite_x=False, workers=None, orthogonalize=None):
    return _execute(_duccfft.dct, x, type, n, axis, norm, 
                    overwrite_x, workers, orthogonalize)


def dct(x, type=2, n=None, axis=-1, norm=None, overwrite_x=False):
    r"""
    Return the Discrete Cosine Transform of arbitrary type sequence x.

    Parameters
    ----------
    x : array_like
        The input array.
    type : {1, 2, 3, 4}, optional
        Type of the DCT (see Notes). Default type is 2.
    n : int, optional
        Length of the transform.  If ``n < x.shape[axis]``, `x` is
        truncated.  If ``n > x.shape[axis]``, `x` is zero-padded. The
        default results in ``n = x.shape[axis]``.
    axis : int, optional
        Axis along which the dct is computed; the default is over the
        last axis (i.e., ``axis=-1``).
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
    idct : Inverse DCT

    Notes
    -----
    For a single dimension array ``x``, ``dct(x, norm='ortho')`` is equal to
    MATLAB ``dct(x)``.

    There are, theoretically, 8 types of the DCT, only the first 4 types are
    implemented in scipy. 'The' DCT generally refers to DCT type 2, and 'the'
    Inverse DCT generally refers to DCT type 3.

    **Type I**

    There are several definitions of the DCT-I; we use the following
    (for ``norm=None``)

    .. math::

       y_k = x_0 + (-1)^k x_{N-1} + 2 \sum_{n=1}^{N-2} x_n \cos\left(
       \frac{\pi k n}{N-1} \right)

    If ``norm='ortho'``, ``x[0]`` and ``x[N-1]`` are multiplied by a scaling
    factor of :math:`\sqrt{2}`, and ``y[k]`` is multiplied by a scaling factor
    ``f``

    .. math::

        f = \begin{cases}
         \frac{1}{2}\sqrt{\frac{1}{N-1}} & \text{if }k=0\text{ or }N-1, \\
         \frac{1}{2}\sqrt{\frac{2}{N-1}} & \text{otherwise} \end{cases}

    .. versionadded:: 1.2.0
       Orthonormalization in DCT-I.

    .. note::
       The DCT-I is only supported for input size > 1.

    **Type II**

    There are several definitions of the DCT-II; we use the following
    (for ``norm=None``)

    .. math::

       y_k = 2 \sum_{n=0}^{N-1} x_n \cos\left(\frac{\pi k(2n+1)}{2N} \right)

    If ``norm='ortho'``, ``y[k]`` is multiplied by a scaling factor ``f``

    .. math::
       f = \begin{cases}
       \sqrt{\frac{1}{4N}} & \text{if }k=0, \\
       \sqrt{\frac{1}{2N}} & \text{otherwise} \end{cases}

    which makes the corresponding matrix of coefficients orthonormal
    (``O @ O.T = np.eye(N)``).

    **Type III**

    There are several definitions, we use the following (for ``norm=None``)

    .. math::

       y_k = x_0 + 2 \sum_{n=1}^{N-1} x_n \cos\left(\frac{\pi(2k+1)n}{2N}\right)

    or, for ``norm='ortho'``

    .. math::

       y_k = \frac{x_0}{\sqrt{N}} + \sqrt{\frac{2}{N}} \sum_{n=1}^{N-1} x_n
       \cos\left(\frac{\pi(2k+1)n}{2N}\right)

    The (unnormalized) DCT-III is the inverse of the (unnormalized) DCT-II, up
    to a factor ``2N``. The orthonormalized DCT-III is exactly the inverse of
    the orthonormalized DCT-II.

    **Type IV**

    There are several definitions of the DCT-IV; we use the following
    (for ``norm=None``)

    .. math::

       y_k = 2 \sum_{n=0}^{N-1} x_n \cos\left(\frac{\pi(2k+1)(2n+1)}{4N} \right)

    If ``norm='ortho'``, ``y[k]`` is multiplied by a scaling factor ``f``

    .. math::

        f = \frac{1}{\sqrt{2N}}

    .. versionadded:: 1.2.0
       Support for DCT-IV.

    References
    ----------
    .. [1] 'A Fast Cosine Transform in One and Two Dimensions', by J.
           Makhoul, `IEEE Transactions on acoustics, speech and signal
           processing` vol. 28(1), pp. 27-34,
           :doi:`10.1109/TASSP.1980.1163351` (1980).
    .. [2] Wikipedia, "Discrete cosine transform",
           https://en.wikipedia.org/wiki/Discrete_cosine_transform

    Examples
    --------
    The Type 1 DCT is equivalent to the FFT (though faster) for real,
    even-symmetrical inputs. The output is also real and even-symmetrical.
    Half of the FFT input is used to generate half of the FFT output:

    >>> from scipy.fftpack import fft, dct
    >>> import numpy as np
    >>> fft(np.array([4., 3., 5., 10., 5., 3.])).real
    array([ 30.,  -8.,   6.,  -2.,   6.,  -8.])
    >>> dct(np.array([4., 3., 5., 10.]), 1)
    array([ 30.,  -8.,   6.,  -2.])

    """
    return _duccfft.dct(x, type, n, axis, norm, overwrite_x)


def dct(x: Array, type: int = 2, n: int | None = None,
        axis: int = -1, norm: str | None = None) -> Array:
  """Computes the discrete cosine transform of the input

  JAX implementation of :func:`scipy.fft.dct`.

  Args:
    x: array
    type: integer, default = 2. Currently only type 2 is supported.
    n: integer, default = x.shape[axis]. The length of the transform.
      If larger than ``x.shape[axis]``, the input will be zero-padded, if
      smaller, the input will be truncated.
    axis: integer, default=-1. The axis along which the dct will be performed.
    norm: string. The normalization mode: one of ``[None, "backward", "ortho"]``.
      The default is ``None``, which is equivalent to ``"backward"``.

  Returns:
    array containing the discrete cosine transform of x

  See Also:
    - :func:`jax.scipy.fft.dctn`: multidimensional DCT
    - :func:`jax.scipy.fft.idct`: inverse DCT
    - :func:`jax.scipy.fft.idctn`: multidimensional inverse DCT

  Examples:
    >>> x = jax.random.normal(jax.random.key(0), (3, 3))
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.scipy.fft.dct(x))
    [[ 6.43  3.56 -2.86]
     [-1.75  1.55 -1.4 ]
     [ 1.33 -2.01 -0.82]]

    When ``n`` smaller than ``x.shape[axis]``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.scipy.fft.dct(x, n=2))
    [[ 7.3  -0.57]
     [ 0.19 -0.36]
     [-0.   -1.4 ]]

    When ``n`` smaller than ``x.shape[axis]`` and ``axis=0``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.scipy.fft.dct(x, n=2, axis=0))
    [[ 3.09  4.4  -2.81]
     [ 2.41  2.62  0.76]]

    When ``n`` larger than ``x.shape[axis]`` and ``axis=1``

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jax.scipy.fft.dct(x, n=4, axis=1))
    [[ 6.43  4.88  0.04 -3.3 ]
     [-1.75  0.73  1.01 -2.18]
     [ 1.33 -1.05 -2.34 -0.07]]
  """
  x = ensure_arraylike("dct", x)

  if type != 2:
    raise NotImplementedError('Only DCT type 2 is implemented.')
  if norm is not None and norm not in ['backward', 'ortho']:
    raise ValueError(f"jax.scipy.fft.dct: {norm=!r} is not implemented")

  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return lax.complex(
      dct(x.real, type=type, n=n, norm=norm, axis=axis),
      dct(x.imag, type=type, n=n, norm=norm, axis=axis),
    )

  axis = canonicalize_axis(axis, x.ndim)
  if n is not None:
    x = lax.pad(x, jnp.array(0, x.dtype),
                [(0, n - x.shape[axis] if a == axis else 0, 0)
                 for a in range(x.ndim)])

  N = x.shape[axis]
  v = _dct_interleave(x, axis)
  V = jnp_fft.fft(v, axis=axis)
  k = lax.expand_dims(jnp.arange(N, dtype=V.real.dtype), [a for a in range(x.ndim) if a != axis])
  out = V * _W4(N, k)
  out = 2 * out.real
  if norm == 'ortho':
    out = _dct_ortho_norm(out, axis)
  return out

