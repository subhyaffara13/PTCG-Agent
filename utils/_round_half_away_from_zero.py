
def _round_half_away_from_zero(a: Array) -> Array:
  return a if dtypes.issubdtype(a.dtype, np.integer) else lax.round(a)

