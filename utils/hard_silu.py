
def hard_silu(x: ArrayLike) -> Array:
  r"""Hard SiLU (swish) activation function

  Computes the element-wise function

  .. math::
    \mathrm{hard\_silu}(x) = x \cdot \mathrm{hard\_sigmoid}(x)

  Both :func:`hard_silu` and :func:`hard_swish` are aliases for the same
  function.

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`hard_sigmoid`
  """
  x_arr = numpy_util.ensure_arraylike("hard_silu", x)
  return x_arr * hard_sigmoid(x_arr)

