
def polydiv(u, v):
    """
    Returns the quotient and remainder of polynomial division.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    The input arrays are the coefficients (including any coefficients
    equal to zero) of the "numerator" (dividend) and "denominator"
    (divisor) polynomials, respectively.

    Parameters
    ----------
    u : array_like or poly1d
        Dividend polynomial's coefficients.

    v : array_like or poly1d
        Divisor polynomial's coefficients.

    Returns
    -------
    q : ndarray
        Coefficients, including those equal to zero, of the quotient.
    r : ndarray
        Coefficients, including those equal to zero, of the remainder.

    See Also
    --------
    poly, polyadd, polyder, polydiv, polyfit, polyint, polymul, polysub
    polyval

    Notes
    -----
    Both `u` and `v` must be 0-d or 1-d (ndim = 0 or 1), but `u.ndim` need
    not equal `v.ndim`. In other words, all four possible combinations -
    ``u.ndim = v.ndim = 0``, ``u.ndim = v.ndim = 1``,
    ``u.ndim = 1, v.ndim = 0``, and ``u.ndim = 0, v.ndim = 1`` - work.

    Examples
    --------

    .. math:: \\frac{3x^2 + 5x + 2}{2x + 1} = 1.5x + 1.75, remainder 0.25

    >>> import numpy as np

    >>> x = np.array([3.0, 5.0, 2.0])
    >>> y = np.array([2.0, 1.0])
    >>> np.polydiv(x, y)
    (array([1.5 , 1.75]), array([0.25]))

    """
    truepoly = (isinstance(u, poly1d) or isinstance(v, poly1d))
    u = atleast_1d(u) + 0.0
    v = atleast_1d(v) + 0.0
    # w has the common type
    w = u[0] + v[0]
    m = len(u) - 1
    n = len(v) - 1
    scale = 1. / v[0]
    q = NX.zeros((max(m - n + 1, 1),), w.dtype)
    r = u.astype(w.dtype)
    for k in range(m - n + 1):
        d = scale * r[k]
        q[k] = d
        r[k:k + n + 1] -= d * v
    while NX.allclose(r[0], 0, rtol=1e-14) and (r.shape[-1] > 1):
        r = r[1:]
    if truepoly:
        return poly1d(q), poly1d(r)
    return q, r


def polydiv(c1, c2):
    """
    Divide one polynomial by another.

    Returns the quotient-with-remainder of two polynomials `c1` / `c2`.
    The arguments are sequences of coefficients, from lowest order term
    to highest, e.g., [1,2,3] represents ``1 + 2*x + 3*x**2``.

    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to high.

    Returns
    -------
    [quo, rem] : ndarrays
        Of coefficient series representing the quotient and remainder.

    See Also
    --------
    polyadd, polysub, polymulx, polymul, polypow

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1, 2, 3)
    >>> c2 = (3, 2, 1)
    >>> P.polydiv(c1, c2)
    (array([3.]), array([-8., -4.]))
    >>> P.polydiv(c2, c1)
    (array([ 0.33333333]), array([ 2.66666667,  1.33333333]))  # may vary

    """
    # c1, c2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])
    if c2[-1] == 0:
        raise ZeroDivisionError  # FIXME: add message with details to exception

    # note: this is more efficient than `pu._div(polymul, c1, c2)`
    lc1 = len(c1)
    lc2 = len(c2)
    if lc1 < lc2:
        return c1[:1] * 0, c1
    elif lc2 == 1:
        return c1 / c2[-1], c1[:1] * 0
    else:
        dlen = lc1 - lc2
        scl = c2[-1]
        c2 = c2[:-1] / scl
        i = dlen
        j = lc1 - 1
        while i >= 0:
            c1[i:j] -= c2 * c1[j]
            i -= 1
            j -= 1
        return c1[j + 1:] / scl, pu.trimseq(c1[:j + 1])


def polydiv(u: ArrayLike, v: ArrayLike, *, trim_leading_zeros: bool = False) -> tuple[Array, Array]:
  r"""Returns the quotient and remainder of polynomial division.

  JAX implementation of :func:`numpy.polydiv`.

  Args:
    u: Array of dividend polynomial coefficients.
    v: Array of divisor polynomial coefficients.
    trim_leading_zeros: Default is ``False``. If ``True`` removes the leading
      zeros in the return value to match the result of numpy. But prevents the
      function from being able to be used in compiled code. Due to differences
      in accumulation of floating point arithmetic errors, the cutoff for values
      to be considered zero may lead to inconsistent results between NumPy and
      JAX, and even between different JAX backends. The result may lead to
      inconsistent output shapes when ``trim_leading_zeros=True``.

  Returns:
    A tuple of quotient and remainder arrays. The dtype of the output is always
    promoted to inexact.

  Note:
    :func:`jax.numpy.polydiv` only accepts arrays as input unlike
    :func:`numpy.polydiv` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.

  Examples:
    >>> x1 = jnp.array([5, 7, 9])
    >>> x2 = jnp.array([4, 1])
    >>> np.polydiv(x1, x2)
    (array([1.25  , 1.4375]), array([7.5625]))
    >>> jnp.polydiv(x1, x2)
    (Array([1.25  , 1.4375], dtype=float32), Array([0.    , 0.    , 7.5625], dtype=float32))

    If ``trim_leading_zeros=True``, the result matches with ``np.polydiv``'s.

    >>> jnp.polydiv(x1, x2, trim_leading_zeros=True)
    (Array([1.25  , 1.4375], dtype=float32), Array([7.5625], dtype=float32))
  """
  u, v = ensure_arraylike("polydiv", u, v)
  u_arr, v_arr = promote_dtypes_inexact(u, v)
  del u, v
  m = len(u_arr) - 1
  n = len(v_arr) - 1
  scale = 1. / v_arr[0]
  q: Array = zeros(max(m - n + 1, 1), dtype = u_arr.dtype) # force same dtype
  for k in range(0, m-n+1):
    d = scale * u_arr[k]
    q = q.at[k].set(d)
    u_arr = u_arr.at[k:k+n+1].add(-d*v_arr)
  if trim_leading_zeros:
    # use the square root of finfo(dtype) to approximate the absolute tolerance used in numpy
    u_arr = trim_zeros_tol(u_arr, tol=sqrt(finfo(u_arr.dtype).eps), trim='f')
  return q, u_arr

