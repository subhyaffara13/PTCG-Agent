
def _float_divmod(x1: ArrayLike, x2: ArrayLike) -> tuple[Array, Array]:
  # see float_divmod in floatobject.c of CPython
  mod = lax.rem(x1, x2)
  x1_corrected = _where(x2 == 0, x1, lax.sub(x1, mod))
  div = lax.div(x1_corrected, x2)

  ind = lax.bitwise_and(mod != 0, lax.sign(x2) != lax.sign(mod))
  mod = lax.select(ind, mod + x2, mod)
  div = lax.select(ind, div - 1.0, div)

  return lax.round(div), mod

