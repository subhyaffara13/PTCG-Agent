
def typecompat(aval_ref: AbstractValue, aval: AbstractValue) -> bool:
  """Determine whether `aval` conforms to `aval_ref`. Ignores weak_type."""
  try:
    return typematch(aval_ref, aval)
  except TypeError:
    return False

