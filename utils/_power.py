
def _power(x1: ArrayLike, x2: ArrayLike) -> Array:
  x1, x2 = promote_shapes("power", x1, x2)  # not dtypes

  # Case 2: bool/integer result
  x1_, x2_ = promote_args_numeric("power", x1, x2)
  if (dtypes.issubdtype(x1_.dtype, np.integer) or
      dtypes.issubdtype(x1_.dtype, np.bool_)):
    assert np.iinfo(x1_.dtype).bits <= 64  # _pow_int_int assumes <=64bit
    return _pow_int_int(x1_, x2_)

  # Case 3: float/complex base with integer power (special autodiff behavior)
  d1, d2 = x1.dtype, x2.dtype
  if dtypes.issubdtype(d1, np.inexact) and dtypes.issubdtype(d2, np.integer):
    return lax.pow(x1, x2)


  # Case 4: do promotion first
  return lax.pow(x1_, x2_)

