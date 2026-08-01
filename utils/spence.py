
def spence(x: Array) -> Array:
  r"""Spence's function, also known as the dilogarithm for real values.

  JAX implementation of :obj:`scipy.special.spence`.

  It is defined to be:

  .. math::
    \mathrm{spence}(x) = \begin{equation}
    \int_1^x \frac{\log(t)}{1 - t}dt
    \end{equation}

  Unlike the SciPy implementation, this is only defined for positive
  real values of `z`. For negative values, `NaN` is returned.

  Args:
    z: An array of type `float32`, `float64`.

  Returns:
    An array with `dtype=z.dtype`.
    computed values of Spence's function.

  Raises:
    TypeError: if elements of array `z` are not in (float32, float64).

  Notes:
  There is a different convention which defines Spence's function by the
  integral:

  .. math::
    \begin{equation}
    -\int_0^z \frac{\log(1 - t)}{t}dt
    \end{equation}

  This is our spence(1 - z).
  """
  x = jnp.asarray(x)
  dtype = lax.dtype(x)
  if dtype not in (np.float32, np.float64):
    raise TypeError(
      f"x.dtype={dtype} is not supported, see docstring for supported types.")
  return _spence(x)

