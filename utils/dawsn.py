
def dawsn(x: ArrayLike) -> Array:
  r"""Dawson's integral.

  JAX implementation of :obj:`scipy.special.dawsn`.

  .. math::

     \mathrm{dawsn}(x) = e^{-x^2} \int_0^x e^{t^2} \, dt

  Args:
    x: arraylike, real-valued.

  Returns:
    array containing values of Dawson's integral.

  See also:
    - :func:`jax.scipy.special.erfcx`
  """
  x, = promote_args_inexact("dawsn", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("dawsn does not support complex-valued inputs.")
  return _dawsn(x)

