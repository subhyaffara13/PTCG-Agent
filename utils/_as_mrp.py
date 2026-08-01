
def _as_mrp(quat: Array) -> Array:
  sign = jnp.where(quat[3] < 0, -1., 1.)
  denominator = 1. + sign * quat[3]
  return sign * quat[:3] / denominator

