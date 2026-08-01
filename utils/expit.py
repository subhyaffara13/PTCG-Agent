
def expit(x: ArrayLike) -> Array:
  r"""The logistic sigmoid (expit) function

  JAX implementation of :obj:`scipy.special.expit`.

  .. math::

     \mathrm{expit}(x) = \frac{1}{1 + e^{-x}}

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of the expit function.
  """
  x, = promote_args_inexact("expit", x)
  return lax.logistic(x)

