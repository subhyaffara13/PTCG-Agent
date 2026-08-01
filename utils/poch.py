
def poch(z: ArrayLike, m: ArrayLike) -> Array:
  r"""The Pochammer symbol.

  JAX implementation of :obj:`scipy.special.poch`.

  .. math::

     \mathrm{poch}(z, m) = (z)_m = \frac{\Gamma(z + m)}{\Gamma(z)}

  where :math:`\Gamma(z)` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    z: arraylike, real-valued
    m: arraylike, real-valued

  Returns:
    array of Pochammer values.

  Notes:
    The JAX version supports only real-valued inputs.
  """
  z, m = promote_args_inexact("poch", z, m)
  if dtypes.issubdtype(z.dtype, np.complexfloating):
    raise ValueError("jnp.poch does not support complex-valued inputs.")

  return jnp.where(m == 0., jnp.array(1, dtype=z.dtype), gamma(z + m) / gamma(z))

