
def dft(xarr):
    """Discrete Fourier Transform. *xarr* is a sequence of complex numbers.
    Yields the components of the corresponding transformed output vector.

    >>> import cmath
    >>> xarr = [1, 2-1j, -1j, -1+2j]  # time domain
    >>> Xarr = [2, -2-2j, -2j, 4+4j]  # frequency domain
    >>> magnitudes, phases = zip(*map(cmath.polar, Xarr))
    >>> all(map(cmath.isclose, dft(xarr), Xarr))
    True

    Inputs are restricted to numeric types that can add and multiply
    with a complex number.  This includes int, float, complex, and
    Fraction, but excludes Decimal.

    See :func:`idft` for the inverse Discrete Fourier Transform.
    """
    N = len(xarr)
    roots_of_unity = [e ** (n / N * tau * -1j) for n in range(N)]
    for k in range(N):
        coeffs = [roots_of_unity[k * n % N] for n in range(N)]
        yield _complex_sumprod(xarr, coeffs)


def dft(n, scale=None):
    """
    Discrete Fourier transform matrix.

    Create the matrix that computes the discrete Fourier transform of a
    sequence [1]_. The nth primitive root of unity used to generate the
    matrix is exp(-2*pi*i/n), where i = sqrt(-1).

    Parameters
    ----------
    n : int
        Size the matrix to create.
    scale : str, optional
        Must be None, 'sqrtn', or 'n'.
        If `scale` is 'sqrtn', the matrix is divided by `sqrt(n)`.
        If `scale` is 'n', the matrix is divided by `n`.
        If `scale` is None (the default), the matrix is not normalized, and the
        return value is simply the Vandermonde matrix of the roots of unity.

    Returns
    -------
    m : (n, n) ndarray
        The DFT matrix.

    Notes
    -----
    When `scale` is None, multiplying a vector by the matrix returned by
    `dft` is mathematically equivalent to (but much less efficient than)
    the calculation performed by `scipy.fft.fft`.

    .. versionadded:: 0.14.0

    References
    ----------
    .. [1] "DFT matrix", https://en.wikipedia.org/wiki/DFT_matrix

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import dft
    >>> np.set_printoptions(precision=2, suppress=True)  # for compact output
    >>> m = dft(5)
    >>> m
    array([[ 1.  +0.j  ,  1.  +0.j  ,  1.  +0.j  ,  1.  +0.j  ,  1.  +0.j  ],
           [ 1.  +0.j  ,  0.31-0.95j, -0.81-0.59j, -0.81+0.59j,  0.31+0.95j],
           [ 1.  +0.j  , -0.81-0.59j,  0.31+0.95j,  0.31-0.95j, -0.81+0.59j],
           [ 1.  +0.j  , -0.81+0.59j,  0.31-0.95j,  0.31+0.95j, -0.81-0.59j],
           [ 1.  +0.j  ,  0.31+0.95j, -0.81+0.59j, -0.81-0.59j,  0.31-0.95j]])
    >>> x = np.array([1, 2, 3, 0, 3])
    >>> m @ x  # Compute the DFT of x
    array([ 9.  +0.j  ,  0.12-0.81j, -2.12+3.44j, -2.12-3.44j,  0.12+0.81j])

    Verify that ``m @ x`` is the same as ``fft(x)``.

    >>> from scipy.fft import fft
    >>> fft(x)     # Same result as m @ x
    array([ 9.  +0.j  ,  0.12-0.81j, -2.12+3.44j, -2.12-3.44j,  0.12+0.81j])
    """
    if scale not in [None, 'sqrtn', 'n']:
        raise ValueError("scale must be None, 'sqrtn', or 'n'; "
                         f"{scale!r} is not valid.")

    omegas = np.exp(-2j * np.pi * np.arange(n) / n).reshape(-1, 1)
    m = omegas ** np.arange(n)
    if scale == 'sqrtn':
        m /= math.sqrt(n)
    elif scale == 'n':
        m /= n
    return m


def dft(n: int, scale: str | None = None, *,
        dtype: DTypeLike | None = None) -> Array:
  r"""Construct an n-by-n discrete Fourier transform matrix.

  JAX implementation of :func:`scipy.linalg.dft`.

  The DFT matrix :math:`W_n` has entries :math:`W_{ij} = \omega^{ij}`, where
  :math:`\omega = e^{-2\pi i / n}` is the primitive n-th root of unity, for
  :math:`0 \le i, j < n`.

  Args:
    n: size of the matrix.
    scale: (optional) ``None`` (default, unscaled), ``'sqrtn'`` (scale by
      :math:`1/\sqrt{n}`, making the matrix unitary), or ``'n'`` (scale by
      :math:`1/n`).
    dtype: (optional) complex floating-point dtype for the output. Defaults to
      JAX's default complex dtype.

  Returns:
    A DFT matrix of shape ``(n, n)``.

  Examples:
    >>> jax.scipy.linalg.dft(4).round(3)
    Array([[ 1.+0.j,  1.+0.j,  1.+0.j,  1.+0.j],
           [ 1.+0.j, -0.-1.j, -1.+0.j,  0.+1.j],
           [ 1.+0.j, -1.+0.j,  1.-0.j, -1.+0.j],
           [ 1.+0.j,  0.+1.j, -1.+0.j, -0.-1.j]], dtype=complex64)
  """
  if scale is not None and scale not in ('sqrtn', 'n'):
    raise ValueError(
        f"scale must be None, 'sqrtn', or 'n'; got {scale!r}.")
  if dtype is None:
    dtype = dtypes.default_complex_dtype()
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "dft")
    if not dtypes.issubdtype(dtype, np.complexfloating):
      raise ValueError(
          f"dtype must be a complex floating-point type; got {dtype}.")
  a = jnp.arange(n, dtype=dtype)
  omegas = jnp.exp(-2j * np.pi * a[:, None] * a[None, :] / n)
  if scale == 'sqrtn':
    omegas = omegas / jnp.sqrt(n)
  elif scale == 'n':
    omegas = omegas / n
  return omegas

