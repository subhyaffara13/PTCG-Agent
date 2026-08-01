
def rad2deg(self: TensorLikeType):
    torch._check(
        not utils.is_complex_dtype(self.dtype),
        lambda: "rad2deg is not supported for complex tensors.",
    )
    M_180_PI = 57.295779513082320876798154814105170332405472466564
    return self * M_180_PI


def rad2deg(x: ArrayLike, /) -> Array:
  r"""Convert angles from radians to degrees.

  JAX implementation of :obj:`numpy.rad2deg`.

  The angle in radians is converted to degrees by:

  .. math::

     rad2deg(x) = x * \frac{180}{pi}

  Args:
    x: scalar or array. Specifies the angle in radians.

  Returns:
    An array containing the angles in degrees.

  See also:
    - :func:`jax.numpy.deg2rad` and :func:`jax.numpy.radians`: Converts the angles
      from degrees to radians.
    - :func:`jax.numpy.degrees`: Alias of ``rad2deg``.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([pi/4, pi/2, 2*pi/3])
    >>> jnp.rad2deg(x)
    Array([ 45.     ,  90.     , 120.00001], dtype=float32)
    >>> x * 180 / pi
    Array([ 45.     ,  90.     , 119.99999], dtype=float32)
  """
  x, = promote_args_inexact("rad2deg", x)
  return lax.mul(x, _lax_const(x, 180 / np.pi))

