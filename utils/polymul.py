
def polymul(a1, a2, *, xp):
    a1, a2 = _poly1d(a1, xp=xp), _poly1d(a2, xp=xp)

    # prefer np.convolve etc, if available
    convolve_func = getattr(xp, 'convolve', None)
    if convolve_func is None:
        from scipy.signal import convolve as convolve_func

    val = convolve_func(a1, a2)
    return val


def polymul(a1, a2):
    """
    Find the product of two polynomials.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Finds the polynomial resulting from the multiplication of the two input
    polynomials. Each input must be either a poly1d object or a 1D sequence
    of polynomial coefficients, from highest to lowest degree.

    Parameters
    ----------
    a1, a2 : array_like or poly1d object
        Input polynomials.

    Returns
    -------
    out : ndarray or poly1d object
        The polynomial resulting from the multiplication of the inputs. If
        either inputs is a poly1d object, then the output is also a poly1d
        object. Otherwise, it is a 1D array of polynomial coefficients from
        highest to lowest degree.

    See Also
    --------
    poly1d : A one-dimensional polynomial class.
    poly, polyadd, polyder, polydiv, polyfit, polyint, polysub, polyval
    convolve : Array convolution. Same output as polymul, but has parameter
               for overlap mode.

    Examples
    --------
    >>> import numpy as np
    >>> np.polymul([1, 2, 3], [9, 5, 1])
    array([ 9, 23, 38, 17,  3])

    Using poly1d objects:

    >>> p1 = np.poly1d([1, 2, 3])
    >>> p2 = np.poly1d([9, 5, 1])
    >>> print(p1)
       2
    1 x + 2 x + 3
    >>> print(p2)
       2
    9 x + 5 x + 1
    >>> print(np.polymul(p1, p2))
       4      3      2
    9 x + 23 x + 38 x + 17 x + 3

    """
    truepoly = (isinstance(a1, poly1d) or isinstance(a2, poly1d))
    a1, a2 = poly1d(a1), poly1d(a2)
    val = NX.convolve(a1, a2)
    if truepoly:
        val = poly1d(val)
    return val


def polymul(c1, c2):
    """
    Multiply one polynomial by another.

    Returns the product of two polynomials `c1` * `c2`.  The arguments are
    sequences of coefficients, from lowest order term to highest, e.g.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2.``

    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of coefficients representing a polynomial, relative to the
        "standard" basis, and ordered from lowest order term to highest.

    Returns
    -------
    out : ndarray
        Of the coefficients of their product.

    See Also
    --------
    polyadd, polysub, polymulx, polydiv, polypow

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1, 2, 3)
    >>> c2 = (3, 2, 1)
    >>> P.polymul(c1, c2)
    array([  3.,   8.,  14.,   8.,   3.])

    """
    # c1, c2 are trimmed copies
    [c1, c2] = pu.as_series([c1, c2])
    ret = np.convolve(c1, c2)
    return pu.trimseq(ret)


def polymul(a1: ArrayLike, a2: ArrayLike, *, trim_leading_zeros: bool = False) -> Array:
  r"""Returns the product of two polynomials.

  JAX implementation of :func:`numpy.polymul`.

  Args:
    a1: 1D array of polynomial coefficients.
    a2: 1D array of polynomial coefficients.
    trim_leading_zeros: Default is ``False``. If ``True`` removes the leading
      zeros in the return value to match the result of numpy. But prevents the
      function from being able to be used in compiled code. Due to differences
      in accumulation of floating point arithmetic errors, the cutoff for values
      to be considered zero may lead to inconsistent results between NumPy and
      JAX, and even between different JAX backends. The result may lead to
      inconsistent output shapes when ``trim_leading_zeros=True``.

  Returns:
    An array of the coefficients of the product of the two polynomials. The dtype
    of the output is always promoted to inexact.

  Note:
    :func:`jax.numpy.polymul` only accepts arrays as input unlike
    :func:`numpy.polymul` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Examples:
    >>> x1 = np.array([2, 1, 0])
    >>> x2 = np.array([0, 5, 0, 3])
    >>> np.polymul(x1, x2)
    array([10,  5,  6,  3,  0])
    >>> jnp.polymul(x1, x2)
    Array([ 0., 10.,  5.,  6.,  3.,  0.], dtype=float32)

    If ``trim_leading_zeros=True``, the result matches with ``np.polymul``'s.

    >>> jnp.polymul(x1, x2, trim_leading_zeros=True)
    Array([10.,  5.,  6.,  3.,  0.], dtype=float32)

    For input arrays of dtype ``complex``:

    >>> x3 = np.array([2., 1+2j, 1-2j])
    >>> x4 = np.array([0, 5, 0, 3])
    >>> np.polymul(x3, x4)
    array([10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j])
    >>> jnp.polymul(x3, x4)
    Array([ 0. +0.j, 10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j],      dtype=complex64)
    >>> jnp.polymul(x3, x4, trim_leading_zeros=True)
    Array([10. +0.j,  5.+10.j, 11.-10.j,  3. +6.j,  3. -6.j], dtype=complex64)
  """
  a1, a2 = ensure_arraylike("polymul", a1, a2)
  a1_arr, a2_arr = promote_dtypes_inexact(a1, a2)
  del a1, a2
  if trim_leading_zeros and (len(a1_arr) > 1 or len(a2_arr) > 1):
    a1_arr, a2_arr = trim_zeros(a1_arr, trim='f'), trim_zeros(a2_arr, trim='f')
  if len(a1_arr) == 0:
    a1_arr = zeros(1, dtype=a2_arr.dtype)
  if len(a2_arr) == 0:
    a2_arr = zeros(1, dtype=a1_arr.dtype)
  return convolve(a1_arr, a2_arr, mode='full')

