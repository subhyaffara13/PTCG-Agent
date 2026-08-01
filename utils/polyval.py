
def polyval(p, x, *, xp):
    """ Old-style polynomial, `np.polyval`
    """
    p = xp.asarray(p)
    x = xp.asarray(x)
    y = xp.zeros_like(x)

    # NB: cannot do `for pv in p` since array API iteration
    # is only defined for 1D arrays.
    for j in range(p.shape[0]):
        y = y * x + p[j, ...]
    return y


def polyval(p, x):
    """
    Evaluate a polynomial at specific values.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    If `p` is of length N, this function returns the value::

        p[0]*x**(N-1) + p[1]*x**(N-2) + ... + p[N-2]*x + p[N-1]

    If `x` is a sequence, then ``p(x)`` is returned for each element of ``x``.
    If `x` is another polynomial then the composite polynomial ``p(x(t))``
    is returned.

    Parameters
    ----------
    p : array_like or poly1d object
       1D array of polynomial coefficients (including coefficients equal
       to zero) from highest degree to the constant term, or an
       instance of poly1d.
    x : array_like or poly1d object
       A number, an array of numbers, or an instance of poly1d, at
       which to evaluate `p`.

    Returns
    -------
    values : ndarray or poly1d
       If `x` is a poly1d instance, the result is the composition of the two
       polynomials, i.e., `x` is "substituted" in `p` and the simplified
       result is returned. In addition, the type of `x` - array_like or
       poly1d - governs the type of the output: `x` array_like => `values`
       array_like, `x` a poly1d object => `values` is also.

    See Also
    --------
    poly1d: A polynomial class.

    Notes
    -----
    Horner's scheme [1]_ is used to evaluate the polynomial. Even so,
    for polynomials of high degree the values may be inaccurate due to
    rounding errors. Use carefully.

    If `x` is a subtype of `ndarray` the return value will be of the same type.

    References
    ----------
    .. [1] I. N. Bronshtein, K. A. Semendyayev, and K. A. Hirsch (Eng.
       trans. Ed.), *Handbook of Mathematics*, New York, Van Nostrand
       Reinhold Co., 1985, pg. 720.

    Examples
    --------
    >>> import numpy as np
    >>> np.polyval([3,0,1], 5)  # 3 * 5**2 + 0 * 5**1 + 1
    76
    >>> np.polyval([3,0,1], np.poly1d(5))
    poly1d([76])
    >>> np.polyval(np.poly1d([3,0,1]), 5)
    76
    >>> np.polyval(np.poly1d([3,0,1]), np.poly1d(5))
    poly1d([76])

    """
    p = NX.asarray(p)
    if isinstance(x, poly1d):
        y = 0
    else:
        x = NX.asanyarray(x)
        y = NX.zeros_like(x)
    for pv in p:
        y = y * x + pv
    return y


def polyval(x, c, tensor=True):
    """
    Evaluate a polynomial at points x.

    If `c` is of length ``n + 1``, this function returns the value

    .. math:: p(x) = c_0 + c_1 * x + ... + c_n * x^n

    The parameter `x` is converted to an array only if it is a tuple or a
    list, otherwise it is treated as a scalar. In either case, either `x`
    or its elements must support multiplication and addition both with
    themselves and with the elements of `c`.

    If `c` is a 1-D array, then ``p(x)`` will have the same shape as `x`.  If
    `c` is multidimensional, then the shape of the result depends on the
    value of `tensor`. If `tensor` is true the shape will be c.shape[1:] +
    x.shape. If `tensor` is false the shape will be c.shape[1:]. Note that
    scalars have shape (,).

    Trailing zeros in the coefficients will be used in the evaluation, so
    they should be avoided if efficiency is a concern.

    Parameters
    ----------
    x : array_like, compatible object
        If `x` is a list or tuple, it is converted to an ndarray, otherwise
        it is left unchanged and treated as a scalar. In either case, `x`
        or its elements must support addition and multiplication with
        with themselves and with the elements of `c`.
    c : array_like
        Array of coefficients ordered so that the coefficients for terms of
        degree n are contained in c[n]. If `c` is multidimensional the
        remaining indices enumerate multiple polynomials. In the two
        dimensional case the coefficients may be thought of as stored in
        the columns of `c`.
    tensor : boolean, optional
        If True, the shape of the coefficient array is extended with ones
        on the right, one for each dimension of `x`. Scalars have dimension 0
        for this action. The result is that every column of coefficients in
        `c` is evaluated for every element of `x`. If False, `x` is broadcast
        over the columns of `c` for the evaluation.  This keyword is useful
        when `c` is multidimensional. The default value is True.

    Returns
    -------
    values : ndarray, compatible object
        The shape of the returned array is described above.

    See Also
    --------
    polyval2d, polygrid2d, polyval3d, polygrid3d

    Notes
    -----
    The evaluation uses Horner's method.

    When using coefficients from polynomials created with ``Polynomial.fit()``,
    use ``p(x)`` or ``polyval(x, p.convert().coef)`` to handle domain/window
    scaling correctly, not ``polyval(x, p.coef)``.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.polynomial.polynomial import polyval
    >>> polyval(1, [1,2,3])
    6.0
    >>> a = np.arange(4).reshape(2,2)
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> polyval(a, [1, 2, 3])
    array([[ 1.,   6.],
           [17.,  34.]])
    >>> coef = np.arange(4).reshape(2, 2)  # multidimensional coefficients
    >>> coef
    array([[0, 1],
           [2, 3]])
    >>> polyval([1, 2], coef, tensor=True)
    array([[2.,  4.],
           [4.,  7.]])
    >>> polyval([1, 2], coef, tensor=False)
    array([2.,  7.])

    """
    c = np.array(c, ndmin=1, copy=None)
    if c.dtype.char in '?bBhHiIlLqQpP':
        # astype fails with NA
        c = c + 0.0
    if isinstance(x, (tuple, list)):
        x = np.asarray(x)
    if isinstance(x, np.ndarray) and tensor:
        c = c.reshape(c.shape + (1,) * x.ndim)

    c0 = c[-1] + x * 0
    for i in range(2, len(c) + 1):
        c0 = c[-i] + c0 * x
    return c0


def polyval(ctx, coeffs, x, derivative=False):
    r"""
    Given coefficients `[c_n, \ldots, c_2, c_1, c_0]` and a number `x`,
    :func:`~mpmath.polyval` evaluates the polynomial

    .. math ::

        P(x) = c_n x^n + \ldots + c_2 x^2 + c_1 x + c_0.

    If *derivative=True* is set, :func:`~mpmath.polyval` simultaneously
    evaluates `P(x)` with the derivative, `P'(x)`, and returns the
    tuple `(P(x), P'(x))`.

        >>> from mpmath import *
        >>> mp.pretty = True
        >>> polyval([3, 0, 2], 0.5)
        2.75
        >>> polyval([3, 0, 2], 0.5, derivative=True)
        (2.75, 3.0)

    The coefficients and the evaluation point may be any combination
    of real or complex numbers.
    """
    if not coeffs:
        return ctx.zero
    p = ctx.convert(coeffs[0])
    q = ctx.zero
    for c in coeffs[1:]:
        if derivative:
            q = p + x*q
        p = c + x*p
    if derivative:
        return p, q
    else:
        return p


def polyval(p: ArrayLike, x: ArrayLike, *, unroll: int = 16) -> Array:
  r"""Evaluates the polynomial at specific values.

  JAX implementations of :func:`numpy.polyval`.

  For the 1D-polynomial coefficients ``p`` of length ``M``, the function returns
  the value:

  .. math::

    p_0 x^{M - 1} + p_1 x^{M - 2} + ... + p_{M - 1}

  Args:
    p: An array of polynomial coefficients of shape ``(M,)``.
    x: A number or an array of numbers.
    unroll: A number used to control the number of unrolled steps with
      ``lax.scan``. It must be specified statically.

  Returns:
    An array of same shape as ``x``.

  Note:

    The ``unroll`` parameter is JAX specific. It does not affect correctness but
    can have a major impact on performance for evaluating high-order polynomials.
    The parameter controls the number of unrolled steps with ``lax.scan`` inside
    the ``jnp.polyval`` implementation. Consider setting ``unroll=128`` (or even
    higher) to improve runtime performance on accelerators, at the cost of
    increased compilation time.

  See also:
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit.
    - :func:`jax.numpy.poly`: Finds the coefficients of a polynomial with given
      roots.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Examples:
    >>> p = jnp.array([2, 5, 1])
    >>> jnp.polyval(p, 3)
    Array(34, dtype=int32)

    If ``x`` is a 2D array, ``polyval`` returns 2D-array with same shape as
    that of ``x``:

    >>> x = jnp.array([[2, 1, 5],
    ...                [3, 4, 7],
    ...                [1, 3, 5]])
    >>> jnp.polyval(p, x)
    Array([[ 19,   8,  76],
           [ 34,  53, 134],
           [  8,  34,  76]], dtype=int32)
  """
  p, x = ensure_arraylike("polyval", p, x)
  p_arr, x_arr = promote_dtypes(p, x)
  del p, x
  shape = lax.broadcast_shapes(p_arr.shape[1:], x_arr.shape)
  y = lax.full_like(x_arr, 0, shape=shape, dtype=x_arr.dtype)
  y, _ = control_flow.scan(lambda y, p: (y * x_arr + p, None), y, p_arr, unroll=unroll)
  return y

