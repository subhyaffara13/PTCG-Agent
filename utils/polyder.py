
def polyder(p, m=1):
    """
    Return the derivative of the specified order of a polynomial.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Parameters
    ----------
    p : poly1d or sequence
        Polynomial to differentiate.
        A sequence is interpreted as polynomial coefficients, see `poly1d`.
    m : int, optional
        Order of differentiation (default: 1)

    Returns
    -------
    der : poly1d
        A new polynomial representing the derivative.

    See Also
    --------
    polyint : Anti-derivative of a polynomial.
    poly1d : Class for one-dimensional polynomials.

    Examples
    --------

    The derivative of the polynomial :math:`x^3 + x^2 + x^1 + 1` is:

    >>> import numpy as np

    >>> p = np.poly1d([1,1,1,1])
    >>> p2 = np.polyder(p)
    >>> p2
    poly1d([3, 2, 1])

    which evaluates to:

    >>> p2(2.)
    17.0

    We can verify this, approximating the derivative with
    ``(f(x + h) - f(x))/h``:

    >>> (p(2. + 0.001) - p(2.)) / 0.001
    17.007000999997857

    The fourth-order derivative of a 3rd-order polynomial is zero:

    >>> np.polyder(p, 2)
    poly1d([6, 2])
    >>> np.polyder(p, 3)
    poly1d([6])
    >>> np.polyder(p, 4)
    poly1d([0])

    """
    m = int(m)
    if m < 0:
        raise ValueError("Order of derivative must be positive (see polyint)")

    truepoly = isinstance(p, poly1d)
    p = NX.asarray(p)
    n = len(p) - 1
    y = p[:-1] * NX.arange(n, 0, -1)
    if m == 0:
        val = p
    else:
        val = polyder(y, m - 1)
    if truepoly:
        val = poly1d(val)
    return val


def polyder(c, m=1, scl=1, axis=0):
    """
    Differentiate a polynomial.

    Returns the polynomial coefficients `c` differentiated `m` times along
    `axis`.  At each iteration the result is multiplied by `scl` (the
    scaling factor is for use in a linear change of variable).  The
    argument `c` is an array of coefficients from low to high degree along
    each axis, e.g., [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2``
    while [[1,2],[1,2]] represents ``1 + 1*x + 2*y + 2*x*y`` if axis=0 is
    ``x`` and axis=1 is ``y``.

    Parameters
    ----------
    c : array_like
        Array of polynomial coefficients. If c is multidimensional the
        different axis correspond to different variables with the degree
        in each axis given by the corresponding index.
    m : int, optional
        Number of derivatives taken, must be non-negative. (Default: 1)
    scl : scalar, optional
        Each differentiation is multiplied by `scl`.  The end result is
        multiplication by ``scl**m``.  This is for use in a linear change
        of variable. (Default: 1)
    axis : int, optional
        Axis over which the derivative is taken. (Default: 0).

    Returns
    -------
    der : ndarray
        Polynomial coefficients of the derivative.

    See Also
    --------
    polyint

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c = (1, 2, 3, 4)
    >>> P.polyder(c)  # (d/dx)(c)
    array([  2.,   6.,  12.])
    >>> P.polyder(c, 3)  # (d**3/dx**3)(c)
    array([24.])
    >>> P.polyder(c, scl=-1)  # (d/d(-x))(c)
    array([ -2.,  -6., -12.])
    >>> P.polyder(c, 2, -1)  # (d**2/d(-x)**2)(c)
    array([  6.,  24.])

    """
    c = np.array(c, ndmin=1, copy=True)
    if c.dtype.char in '?bBhHiIlLqQpP':
        # astype fails with NA
        c = c + 0.0
    cdt = c.dtype
    cnt = pu._as_int(m, "the order of derivation")
    iaxis = pu._as_int(axis, "the axis")
    if cnt < 0:
        raise ValueError("The order of derivation must be non-negative")
    iaxis = np.lib.array_utils.normalize_axis_index(iaxis, c.ndim)

    if cnt == 0:
        return c

    c = np.moveaxis(c, iaxis, 0)
    n = len(c)
    if cnt >= n:
        c = c[:1] * 0
    else:
        for i in range(cnt):
            n = n - 1
            c *= scl
            der = np.empty((n,) + c.shape[1:], dtype=cdt)
            for j in range(n, 0, -1):
                der[j - 1] = j * c[j]
            c = der
    c = np.moveaxis(c, 0, iaxis)
    return c


def polyder(p: ArrayLike, m: int = 1) -> Array:
  r"""Returns the coefficients of the derivative of specified order of a polynomial.

  JAX implementation of :func:`numpy.polyder`.

  Args:
    p: Array of polynomials coefficients.
    m: Order of differentiation (positive integer). Default is 1. It must be
      specified statically.

  Returns:
    An array of polynomial coefficients representing the derivative.

  Note:
    :func:`jax.numpy.polyder` differs from :func:`numpy.polyder` when an integer
    array is given. NumPy returns the result with dtype ``int`` whereas JAX
    returns the result with dtype ``float``.

  See also:
    - :func:`jax.numpy.polyint`: Computes the integral of polynomial.
    - :func:`jax.numpy.polyval`: Evaluates a polynomial at specific values.

  Examples:

    The first order derivative of the polynomial :math:`2 x^3 - 5 x^2 + 3 x - 1`
    is :math:`6 x^2 - 10 x +3`:

    >>> p = jnp.array([2, -5, 3, -1])
    >>> jnp.polyder(p)
    Array([  6., -10.,   3.], dtype=float32)

    and its second order derivative is :math:`12 x - 10`:

    >>> jnp.polyder(p, m=2)
    Array([ 12., -10.], dtype=float32)
  """
  p = ensure_arraylike("polyder", p)
  m = core.concrete_or_error(operator.index, m, "'m' argument of jnp.polyder")
  p_arr, = promote_dtypes_inexact(p)
  del p
  if m < 0:
    raise ValueError("Order of derivative must be positive")
  if m == 0:
    return p_arr
  coeff = (arange(m, len(p_arr), dtype=p_arr.dtype)[np.newaxis]
          - arange(m, dtype=p_arr.dtype)[:, np.newaxis]).prod(0)
  return p_arr[:-m] * coeff[::-1]

