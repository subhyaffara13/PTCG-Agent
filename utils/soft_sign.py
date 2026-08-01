
def soft_sign(x: ArrayLike) -> Array:
  r"""Soft-sign activation function.

  Computes the element-wise function

  .. math::
    \mathrm{soft\_sign}(x) = \frac{x}{|x| + 1}

  Args:
    x : input array
  """
  x_arr = numpy_util.ensure_arraylike("soft_sign", x)
  return x_arr / (jnp.abs(x_arr) + 1)

