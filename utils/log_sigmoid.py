
def log_sigmoid(g: jit_utils.GraphContext, input):
    p = g.op("Sigmoid", input)
    return g.op("Log", p)


def log_sigmoid(x: ArrayLike) -> Array:
  r"""Log-sigmoid activation function.

  Computes the element-wise function:

  .. math::
    \mathrm{log\_sigmoid}(x) = \log(\mathrm{sigmoid}(x)) = -\log(1 + e^{-x})

  Args:
    x : input array

  Returns:
    An array.

  See also:
    :func:`sigmoid`
  """
  x_arr = numpy_util.ensure_arraylike("log_sigmoid", x)
  return -softplus(-x_arr)

