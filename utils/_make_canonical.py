
def _make_canonical(quat: Array) -> Array:
  is_neg = quat < 0
  is_zero = quat == 0

  neg = (
      is_neg[3]
      | (is_zero[3] & is_neg[0])
      | (is_zero[3] & is_zero[0] & is_neg[1])
      | (is_zero[3] & is_zero[0] & is_zero[1] & is_neg[2])
  )

  return jnp.where(neg, -quat, quat)

