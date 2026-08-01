
def wofz(z: ArrayLike) -> Array:
  r"""Faddeeva function.

  JAX implementation of :obj:`scipy.special.wofz`.

  .. math::

     \mathrm{wofz}(z) = e^{-z^2} \mathrm{erfc}(-iz)

  Args:
    z: arraylike, real or complex.

  Returns:
    array of complex values of the Faddeeva function.

  See also:
    - :func:`jax.scipy.special.erfcx`
  """
  z, = promote_args_complex("wofz", z)
  return _wofz(z)

