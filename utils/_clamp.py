
def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def _clamp(min, operand, max):
  res = jnp.maximum(operand, min)
  return jnp.minimum(res, max)

