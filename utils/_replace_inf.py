
def _replace_inf(x):
    # Replace `np.inf` with kHighsInf
    infs = np.isinf(x)
    with np.errstate(invalid="ignore"):
        x[infs] = np.sign(x[infs])*kHighsInf
    return x


def _replace_inf(x: Array) -> Array:
  re_x = lax.real(x) if dtypes.issubdtype(x.dtype, np.complexfloating) else x
  inf = lax._const(re_x, float('inf'))
  return lax.select(lax.eq(re_x, inf), lax._zeros(x), x)


def _replace_inf(x: ArrayLike) -> Array:
  return lax.select(isposinf(real(x)), lax._zeros(x), x)

