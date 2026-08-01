
def log1mexp(x: ArrayLike) -> Array:
  r"""Numerically stable calculation of :math:`\log(1 - \exp(-x))`.

  This function is undefined for :math:`x < 0`.

  Based on `TensorFlow's implementation <https://www.tensorflow.org/probability/api_docs/python/tfp/math/log1mexp>`_.

  References:
    .. [1] Martin Mächler. `Accurately Computing log(1 − exp(−|a|)) Assessed by the Rmpfr package.
      <https://cran.r-project.org/web/packages/Rmpfr/vignettes/log1mexp-note.pdf>`_.
  """
  x = numpy_util.ensure_arraylike("log1mexp", x)
  c = jnp.log(2.0)
  return jnp.where(
      x < c,
      jnp.log(-jnp.expm1(-x)),
      jnp.log1p(-jnp.exp(-x)),
  )

