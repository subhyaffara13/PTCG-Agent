
def _fori_cond_fun(loop_carry):
  i, upper, _ = loop_carry
  return lax.lt(i, upper)

