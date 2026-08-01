
def Arcsin(name, a=0, b=1):
    r"""
    Create a Continuous Random Variable with an arcsin distribution.

    The density of the arcsin distribution is given by

    .. math::
        f(x) := \frac{1}{\pi\sqrt{(x-a)(b-x)}}

    with :math:`x \in (a,b)`. It must hold that :math:`-\infty < a < b < \infty`.

    Parameters
    ==========

    a : Real number, the left interval boundary
    b : Real number, the right interval boundary

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Arcsin, density, cdf
    >>> from sympy import Symbol

    >>> a = Symbol("a", real=True)
    >>> b = Symbol("b", real=True)
    >>> z = Symbol("z")

    >>> X = Arcsin("x", a, b)

    >>> density(X)(z)
    1/(pi*sqrt((-a + z)*(b - z)))

    >>> cdf(X)(z)
    Piecewise((0, a > z),
            (2*asin(sqrt((-a + z)/(-a + b)))/pi, b >= z),
            (1, True))


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Arcsine_distribution

    """

    return rv(name, ArcsinDistribution, (a, b))


def arcsin(x):
    """
    Compute the inverse sine of x.

    Return the "principal value" (for a description of this, see
    `numpy.arcsin`) of the inverse sine of `x`. For real `x` such that
    `abs(x) <= 1`, this is a real number in the closed interval
    :math:`[-\\pi/2, \\pi/2]`.  Otherwise, the complex principle value is
    returned.

    Parameters
    ----------
    x : array_like or scalar
       The value(s) whose arcsin is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The inverse sine(s) of the `x` value(s). If `x` was a scalar, so
       is `out`, otherwise an array object is returned.

    See Also
    --------
    numpy.arcsin

    Notes
    -----
    For an arcsin() that returns ``NAN`` when real `x` is not in the
    interval ``[-1,1]``, use `numpy.arcsin`.

    Examples
    --------
    >>> import numpy as np
    >>> np.set_printoptions(precision=4)

    >>> np.emath.arcsin(0)
    0.0

    >>> np.emath.arcsin([0,1])
    array([0.    , 1.5708])

    """
    x = _fix_real_abs_gt_1(x)
    return nx.arcsin(x)


def arcsin(x: ArrayLike, /) -> Array:
  r"""Compute element-wise inverse of trigonometric sine of input.

  JAX implementation of :obj:`numpy.arcsin`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the inverse trigonometric sine of each element of ``x``
    in radians in the range ``[-pi/2, pi/2]``, promoting to inexact dtype.

  Note:
    - ``jnp.arcsin`` returns ``nan`` when ``x`` is real-valued and not in the closed
      interval ``[-1, 1]``.
    - ``jnp.arcsin`` follows the branch cut convention of :obj:`numpy.arcsin` for
      complex inputs.

  See also:
    - :func:`jax.numpy.sin`: Computes a trigonometric sine of each element of input.
    - :func:`jax.numpy.arccos` and :func:`jax.numpy.acos`: Computes the inverse of
      trigonometric cosine of each element of input.
    - :func:`jax.numpy.arctan` and :func:`jax.numpy.atan`: Computes the inverse of
      trigonometric tangent of each element of input.

  Examples:
    >>> x = jnp.array([-2, -1, -0.5, 0, 0.5, 1, 2])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arcsin(x)
    Array([   nan, -1.571, -0.524,  0.   ,  0.524,  1.571,    nan], dtype=float32)

    For complex-valued inputs:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arcsin(3+4j)
    Array(0.634+2.306j, dtype=complex64, weak_type=True)
  """
  out = lax.asin(*promote_args_inexact('arcsin', x))
  jnp_error._set_error_if_nan(out)
  return out

