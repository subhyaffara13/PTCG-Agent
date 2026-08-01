
def arccos(x):
    """
    Compute the inverse cosine of x.

    Return the "principal value" (for a description of this, see
    `numpy.arccos`) of the inverse cosine of `x`. For real `x` such that
    `abs(x) <= 1`, this is a real number in the closed interval
    :math:`[0, \\pi]`.  Otherwise, the complex principle value is returned.

    Parameters
    ----------
    x : array_like or scalar
       The value(s) whose arccos is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The inverse cosine(s) of the `x` value(s). If `x` was a scalar, so
       is `out`, otherwise an array object is returned.

    See Also
    --------
    numpy.arccos

    Notes
    -----
    For an arccos() that returns ``NAN`` when real `x` is not in the
    interval ``[-1,1]``, use `numpy.arccos`.

    Examples
    --------
    >>> import numpy as np
    >>> np.set_printoptions(precision=4)

    >>> np.emath.arccos(1) # a scalar is returned
    0.0

    >>> np.emath.arccos([1,2])
    array([0.-0.j   , 0.-1.317j])

    """
    x = _fix_real_abs_gt_1(x)
    return nx.arccos(x)


def arccos(x: ArrayLike, /) -> Array:
  """Compute element-wise inverse of trigonometric cosine of input.

  JAX implementation of :obj:`numpy.arccos`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the inverse trigonometric cosine of each element of ``x``
    in radians in the range ``[0, pi]``, promoting to inexact dtype.

  Note:
    - ``jnp.arccos`` returns ``nan`` when ``x`` is real-valued and not in the closed
      interval ``[-1, 1]``.
    - ``jnp.arccos`` follows the branch cut convention of :obj:`numpy.arccos` for
      complex inputs.

  See also:
    - :func:`jax.numpy.cos`: Computes a trigonometric cosine of each element of
      input.
    - :func:`jax.numpy.arcsin` and :func:`jax.numpy.asin`: Computes the inverse of
      trigonometric sine of each element of input.
    - :func:`jax.numpy.arctan` and :func:`jax.numpy.atan`: Computes the inverse of
      trigonometric tangent of each element of input.

  Examples:
    >>> x = jnp.array([-2, -1, -0.5, 0, 0.5, 1, 2])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arccos(x)
    Array([  nan, 3.142, 2.094, 1.571, 1.047, 0.   ,   nan], dtype=float32)

    For complex inputs:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arccos(4-1j)
    Array(0.252+2.097j, dtype=complex64, weak_type=True)
  """
  out = lax.acos(*promote_args_inexact('arccos', x))
  jnp_error._set_error_if_nan(out)
  return out

