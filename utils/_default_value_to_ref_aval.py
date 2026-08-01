
def _default_value_to_ref_aval(x: Any) -> tuple[AbstractRef, Array]:
  # Default type mapping just creates an AbstractRef from the array's aval.
  aval = core.typeof(x)
  return AbstractRef(aval), x

