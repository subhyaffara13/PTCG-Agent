
def deg2rad(self: TensorLikeType):
    torch._check(
        not utils.is_complex_dtype(self.dtype),
        lambda: "deg2rad is not supported for complex tensors.",
    )
    M_PI_180 = 0.017453292519943295769236907684886127134428718885417
    return self * M_PI_180


def deg2rad(x: ArrayLike, /) -> Array:
  r"""Convert angles from degrees to radians.

  JAX implementation of :obj:`numpy.deg2rad`.

  The angle in degrees is converted to radians by:

  .. math::

     deg2rad(x) = x * \frac{pi}{180}

  Args:
    x: scalar or array. Specifies the angle in degrees.

  Returns:
    An array containing the angles in radians.

  See also:
    - :func:`jax.numpy.rad2deg` and :func:`jax.numpy.degrees`: Converts the angles
      from radians to degrees.
    - :func:`jax.numpy.radians`: Alias of ``deg2rad``.

  Examples:
    >>> x = jnp.array([60, 90, 120, 180])
    >>> jnp.deg2rad(x)
    Array([1.0471976, 1.5707964, 2.0943952, 3.1415927], dtype=float32)
    >>> x * jnp.pi / 180
    Array([1.0471976, 1.5707964, 2.0943952, 3.1415927],      dtype=float32, weak_type=True)
  """
  x, = promote_args_inexact("deg2rad", x)
  return lax.mul(x, _lax_const(x, np.pi / 180))

