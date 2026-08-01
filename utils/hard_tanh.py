
def hard_tanh(x: ArrayLike) -> Array:
  r"""Hard :math:`\mathrm{tanh}` activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{hard\_tanh}(x) = \begin{cases}
      -1, & x < -1\\
      x, & -1 \le x \le 1\\
      1, & 1 < x
    \end{cases}

  Args:
    x : input array

  Returns:
    An array.
  """
  x_arr = numpy_util.ensure_arraylike("hard_tanh", x)
  return jnp.where(x_arr > 1, 1, jnp.where(x_arr < -1, -1, x_arr))

