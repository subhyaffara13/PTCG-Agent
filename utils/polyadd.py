
def polyadd(a1, a2):
    """
    Find the sum of two polynomials.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Returns the polynomial resulting from the sum of two input polynomials.
    Each input must be either a poly1d object or a 1D sequence of polynomial
    coefficients, from highest to lowest degree.

    Parameters
    ----------
    a1, a2 : array_like or poly1d object
        Input polynomials.

    Returns
    -------
    out : ndarray or poly1d object
        The sum of the inputs. If either input is a poly1d object, then the
        output is also a poly1d object. Otherwise, it is a 1D array of
        polynomial coefficients from highest to lowest degree.

    See Also
    --------
    poly1d : A one-dimensional polynomial class.
    poly, polyadd, polyder, polydiv, polyfit, polyint, polysub, polyval

    Examples
    --------
    >>> import numpy as np
    >>> np.polyadd([1, 2], [9, 5, 4])
    array([9, 6, 6])

    Using poly1d objects:

    >>> p1 = np.poly1d([1, 2])
    >>> p2 = np.poly1d([9, 5, 4])
    >>> print(p1)
    1 x + 2
    >>> print(p2)
       2
    9 x + 5 x + 4
    >>> print(np.polyadd(p1, p2))
       2
    9 x + 6 x + 6

    """
    truepoly = (isinstance(a1, poly1d) or isinstance(a2, poly1d))
    a1 = atleast_1d(a1)
    a2 = atleast_1d(a2)
    diff = len(a2) - len(a1)
    if diff == 0:
        val = a1 + a2
    elif diff > 0:
        zr = NX.zeros(diff, a1.dtype)
        val = NX.concatenate((zr, a1)) + a2
    else:
        zr = NX.zeros(abs(diff), a2.dtype)
        val = a1 + NX.concatenate((zr, a2))
    if truepoly:
        val = poly1d(val)
    return val


def polyadd(c1, c2):
    """
    Add one polynomial to another.

    Returns the sum of two polynomials `c1` + `c2`.  The arguments are
    sequences of coefficients from lowest order term to highest, i.e.,
    [1,2,3] represents the polynomial ``1 + 2*x + 3*x**2``.

    Parameters
    ----------
    c1, c2 : array_like
        1-D arrays of polynomial coefficients ordered from low to high.

    Returns
    -------
    out : ndarray
        The coefficient array representing their sum.

    See Also
    --------
    polysub, polymulx, polymul, polydiv, polypow

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c1 = (1, 2, 3)
    >>> c2 = (3, 2, 1)
    >>> sum = P.polyadd(c1,c2); sum
    array([4.,  4.,  4.])
    >>> P.polyval(2, sum)  # 4 + 4(2) + 4(2**2)
    28.0

    """
    return pu._add(c1, c2)


def polyadd(a1: ArrayLike, a2: ArrayLike) -> Array:
  r"""Returns the sum of the two polynomials.

  JAX implementation of :func:`numpy.polyadd`.

  Args:
    a1: Array of polynomial coefficients.
    a2: Array of polynomial coefficients.

  Returns:
    An array containing the coefficients of the sum of input polynomials.

  Note:
    :func:`jax.numpy.polyadd` only accepts arrays as input unlike
    :func:`numpy.polyadd` which accepts scalar inputs as well.

  See also:
    - :func:`jax.numpy.polysub`: Computes the difference of two polynomials.
    - :func:`jax.numpy.polymul`: Computes the product of two polynomials.
    - :func:`jax.numpy.polydiv`: Computes the quotient and remainder of polynomial
      division.

  Examples:
    >>> x1 = jnp.array([2, 3])
    >>> x2 = jnp.array([5, 4, 1])
    >>> jnp.polyadd(x1, x2)
    Array([5, 6, 4], dtype=int32)

    >>> x3 = jnp.array([[2, 3, 1]])
    >>> x4 = jnp.array([[5, 7, 3],
    ...                 [8, 2, 6]])
    >>> jnp.polyadd(x3, x4)
    Array([[ 5,  7,  3],
           [10,  5,  7]], dtype=int32)

    >>> x5 = jnp.array([1, 3, 5])
    >>> x6 = jnp.array([[5, 7, 9],
    ...                 [8, 6, 4]])
    >>> jnp.polyadd(x5, x6)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: Cannot broadcast to shape with fewer dimensions: arr_shape=(2, 3) shape=(2,)
    >>> x7 = jnp.array([2])
    >>> jnp.polyadd(x6, x7)
    Array([[ 5,  7,  9],
           [10,  8,  6]], dtype=int32)
  """
  a1, a2 = ensure_arraylike("polyadd", a1, a2)
  a1_arr, a2_arr = promote_dtypes(a1, a2)
  del a1, a2
  if a2_arr.shape[0] <= a1_arr.shape[0]:
    return a1_arr.at[-a2_arr.shape[0]:].add(a2_arr)
  else:
    return a2_arr.at[-a1_arr.shape[0]:].add(a1_arr)

