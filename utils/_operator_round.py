
def _operator_round(number: ArrayLike, ndigits: int | None = None) -> Array:
  out = lax_numpy.round(number, decimals=ndigits or 0)
  # If `ndigits` is None, for a builtin float round(7.5) returns an integer.
  return out.astype(int) if ndigits is None else out

