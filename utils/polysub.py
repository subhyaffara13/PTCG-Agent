
def polysub(a1, a2):
    """
    Difference (subtraction) of two polynomials.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Given two polynomials `a1` and `a2`, returns ``a1 - a2``.
    `a1` and `a2` can be either array_like sequences of the polynomials'
    coefficients (including coefficients equal to zero), or `poly1d` objects.

    Parameters
    ----------
    a1, a2 : array_like or poly1d
        Minuend and subtrahend polynomials, respectively.

    Returns
    -------
    out : ndarray or poly1d
        Array or `poly1d` object of the difference polynomial's coefficients.

    See Also
    --------
    polyval, polydiv, polymul, polyadd

    Examples
    --------

    .. math:: (2 x^2 + 10 x - 2) - (3 x^2 + 10 x -4) = (-x^2 + 2)

    >>> import numpy as np

    >>> np.polysub([2, 10, -2], [3, 10, -4])
    array([-1,  0,  2])

    """
    truepoly = (isinstance(a1, poly1d) or isinstance(a2, poly1d))
    a1 = atleast_1d(a1)
    a2 = atleast_1d(a2)
    diff = len(a2) - len(a1)
    if diff == 0:
        val = a1 - a2
    elif diff > 0:
        zr = NX.zeros(diff, a1.dtype)
        val = NX.concatenate((zr, a1)) - a2
    else:
        zr = NX.zeros(abs(diff), a2.dtype)
        val = a1 - NX.concatenate((zr, a2))
    if truepoly:
        val = poly1d(val)
    return val


def polysub(c1, c2):
    """
    Subtract one polynomial from another.

    Returns the difference of two polynomials `c1` - `c2`.  The arguments
    are sequences of coefficients from lowest order term to highest, i.e.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2``.

    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to
        high.

    Returns
    -------
    out : ndarray
        Of coefficients representing their difference.

    See Also
    --------
    polyadd, polymulx, polymul, polydiv, polypow

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1, 2, 3)
    >>> c2 = (3, 2, 1)
    >>> P.polysub(c1,c2)
    array([-2.,  0.,  2.])
    >>> P.polysub(c2, c1)  # -P.polysub(c1,c2)
    array([ 2.,  0., -2.])

    """
    return pu._sub(c1, c2)


def polysub(a1: ArrayLike, a2: ArrayLike) -> Array:
  r"""Returns the difference of two polynomials.

  JAX implementation of :func:`numpy.polysub`.

  Args:
    a1: Array of minuend polynomial coefficients.
    a2: Array of subtrahend polynomial coefficients.

  Returns:
    An array containing the coefficients of the difference of two polynomials.

  Note:
    :func:`jax.numpy.polysub` only accepts arrays as input unlike
    :func:`numpy.polysub` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polyadd`: Computes the sum of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Examples:
    >>> x1 = jnp.array([2, 3])
    >>> x2 = jnp.array([5, 4, 1])
    >>> jnp.polysub(x1, x2)
    Array([-5, -2,  2], dtype=int32)

    >>> x3 = jnp.array([[2, 3, 1]])
    >>> x4 = jnp.array([[5, 7, 3],
    ...                 [8, 2, 6]])
    >>> jnp.polysub(x3, x4)
    Array([[-5, -7, -3],
           [-6,  1, -5]], dtype=int32)

    >>> x5 = jnp.array([1, 3, 5])
    >>> x6 = jnp.array([[5, 7, 9],
    ...                 [8, 6, 4]])
    >>> jnp.polysub(x5, x6)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: Cannot broadcast to shape with fewer dimensions: arr_shape=(2, 3) shape=(2,)
    >>> x7 = jnp.array([2])
    >>> jnp.polysub(x6, x7)
    Array([[5, 7, 9],
           [6, 4, 2]], dtype=int32)
  """
  a1, a2 = ensure_arraylike("polysub", a1, a2)
  a1, a2 = promote_dtypes(a1, a2)
  return polyadd(a1, -a2)

