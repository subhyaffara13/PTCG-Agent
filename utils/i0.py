
def i0(x: ArrayLike):
    return torch.special.i0(x)


def i0(a):
    return prims.bessel_i0(a)


def i0(x):
    """
    Modified Bessel function of the first kind, order 0.

    Usually denoted :math:`I_0`.

    Parameters
    ----------
    x : array_like of float
        Argument of the Bessel function.

    Returns
    -------
    out : ndarray, shape = x.shape, dtype = float
        The modified Bessel function evaluated at each of the elements of `x`.

    See Also
    --------
    scipy.special.i0, scipy.special.iv, scipy.special.ive

    Notes
    -----
    The scipy implementation is recommended over this function: it is a
    proper ufunc written in C, and more than an order of magnitude faster.

    We use the algorithm published by Clenshaw [1]_ and referenced by
    Abramowitz and Stegun [2]_, for which the function domain is
    partitioned into the two intervals [0,8] and (8,inf), and Chebyshev
    polynomial expansions are employed in each interval. Relative error on
    the domain [0,30] using IEEE arithmetic is documented [3]_ as having a
    peak of 5.8e-16 with an rms of 1.4e-16 (n = 30000).

    References
    ----------
    .. [1] C. W. Clenshaw, "Chebyshev series for mathematical functions", in
           *National Physical Laboratory Mathematical Tables*, vol. 5, London:
           Her Majesty's Stationery Office, 1962.
    .. [2] M. Abramowitz and I. A. Stegun, *Handbook of Mathematical
           Functions*, 10th printing, New York: Dover, 1964, pp. 379.
           https://personal.math.ubc.ca/~cbm/aands/page_379.htm
    .. [3] https://metacpan.org/pod/distribution/Math-Cephes/lib/Math/Cephes.pod#i0:-Modified-Bessel-function-of-order-zero

    Examples
    --------
    >>> import numpy as np
    >>> np.i0(0.)
    array(1.0)
    >>> np.i0([0, 1, 2, 3])
    array([1.        , 1.26606588, 2.2795853 , 4.88079259])

    """
    x = np.asanyarray(x)
    if x.dtype.kind == 'c':
        raise TypeError("i0 not supported for complex values")
    if x.dtype.kind != 'f':
        x = x.astype(float)
    x = np.abs(x)
    return piecewise(x, [x <= 8.0], [_i0_1, _i0_2])


def i0(x: ArrayLike) -> Array:
  r"""Calculate modified Bessel function of first kind, zeroth order.

  JAX implementation of :func:`numpy.i0`.

  Modified Bessel function of first kind, zeroth order is defined by:

  .. math::

     \mathrm{i0}(x) = I_0(x) = \sum_{k=0}^{\infty} \frac{(x^2/4)^k}{(k!)^2}

  Args:
    x: scalar or array. Specifies the argument of Bessel function. Complex inputs
      are not supported.

  Returns:
    An array containing the corresponding values of the modified Bessel function
    of ``x``.

  See also:
    - :func:`jax.scipy.special.i0`: Calculates the modified Bessel function of
      zeroth order.
    - :func:`jax.scipy.special.i1`: Calculates the modified Bessel function of
      first order.
    - :func:`jax.scipy.special.i0e`: Calculates the exponentially scaled modified
      Bessel function of zeroth order.

  Examples:
    >>> x = jnp.array([-2, -1, 0, 1, 2])
    >>> jnp.i0(x)
    Array([2.2795851, 1.266066 , 1.0000001, 1.266066 , 2.2795851], dtype=float32)
  """
  x_arr, = util.promote_args_inexact("i0", x)
  if not issubdtype(x_arr.dtype, np.floating):
    raise ValueError(f"Unsupported input type to jax.numpy.i0: {x_arr.dtype}")
  return _i0(x_arr)


def i0(x: ArrayLike) -> Array:
  r"""Modified bessel function of zeroth order.

  JAX implementation of :obj:`scipy.special.i0`.

  .. math::

     \mathrm{i0}(x) = I_0(x) = \sum_{k=0}^\infty \frac{(x^2/4)^k}{(k!)^2}

  Args:
    x: array, real-valued

  Returns:
    array of bessel function values.

  See also:
    - :func:`jax.scipy.special.i0e`
    - :func:`jax.scipy.special.i1`
    - :func:`jax.scipy.special.i1e`
  """
  x, = promote_args_inexact("i0", x)
  return lax.mul(lax.exp(lax.abs(x)), lax.bessel_i0e(x))

