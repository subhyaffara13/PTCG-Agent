
def neg(a):
    return prims.neg(a)


def neg(g: jit_utils.GraphContext, self):
    return g.op("Neg", self)


def neg(x: ArrayLike) -> Array:
  r"""Elementwise negation: :math:`-x`.

  This function lowers directly to the `stablehlo.negate`_ operation.

  Args:
    x: input array

  Returns:
    Array of same shape and dtype as ``x``, containing the element-wise negative.

  Notes:
    For unsigned integer inputs, this function returns ``2 ** nbits - x``, where
    ``nbits`` is the number of bits in the integer representation.

  .. _stablehlo.negate: https://openxla.org/stablehlo/spec#negate
  """
  return neg_p.bind(x)

