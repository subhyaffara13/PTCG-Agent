
def arctan(z, rho, cost_only):
    rho[0] = np.arctan(z)
    if cost_only:
        return
    t = 1 + z**2
    rho[1] = 1 / t
    rho[2] = -2 * z / t**2


def arctan(x: ArrayLike, /) -> Array:
  """Compute element-wise inverse of trigonometric tangent of input.

  JAX implement of :obj:`numpy.arctan`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the inverse trigonometric tangent of each element ``x``
    in radians in the range ``[-pi/2, pi/2]``, promoting to inexact dtype.

  Note:
    ``jnp.arctan`` follows the branch cut convention of :obj:`numpy.arctan` for
    complex inputs.

  See also:
    - :func:`jax.numpy.tan`: Computes a trigonometric tangent of each element of
      input.
    - :func:`jax.numpy.arcsin` and :func:`jax.numpy.asin`: Computes the inverse of
      trigonometric sine of each element of input.
    - :func:`jax.numpy.arccos` and :func:`jax.numpy.atan`: Computes the inverse of
      trigonometric cosine of each element of input.

  Examples:
    >>> x = jnp.array([-jnp.inf, -20, -1, 0, 1, 20, jnp.inf])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arctan(x)
    Array([-1.571, -1.521, -0.785,  0.   ,  0.785,  1.521,  1.571], dtype=float32)

    For complex-valued inputs:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arctan(2+7j)
    Array(1.532+0.133j, dtype=complex64, weak_type=True)
  """
  return lax.atan(*promote_args_inexact('arctan', x))

