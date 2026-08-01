
def integer_pow(x: ArrayLike, y: int) -> Array:
  r"""Elementwise power: :math:`x^y`, where :math:`y` is a static integer.

  This will lower to a sequence of :math:`O[\log_2(y)]` repetitions of
  `stablehlo.multiply`_.

  Args:
    x: Input array giving the base value. Must have numerical dtype.
    y: Static scalar integer giving the exponent.

  Returns:
    An array of the same shape and dtype as ``x`` containing the elementwise power.

  See also:
    :func:`jax.lax.pow`: Elementwise power where ``y`` is an array.

  .. _stablehlo.multiply: https://openxla.org/stablehlo/spec#multiply
  """
  return integer_pow_p.bind(x, y=y)

