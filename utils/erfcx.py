
def erfcx(a: TensorLikeType) -> TensorLikeType:
    return prims.erfcx(a)


def erfcx(x: ArrayLike) -> Array:
  r"""Scaled complementary error function.

  JAX implementation of :obj:`scipy.special.erfcx`.

  .. math::

     \mathrm{erfcx}(x) = e^{x^2} \mathrm{erfc}(x)

  This is numerically stable for large positive ``x``, unlike the naive
  formula which overflows.

  Args:
    x: arraylike, real or complex.

  Returns:
    array containing values of the scaled complementary error function.

  See also:
    - :func:`jax.scipy.special.erfc`
    - :func:`jax.scipy.special.erf`
    - :func:`jax.scipy.special.wofz`
  """
  x, = promote_args_inexact("erfcx", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    iz = lax.complex(lax.neg(lax.imag(x)), lax.real(x))
    return _wofz(iz)
  return _erfcx(x)

