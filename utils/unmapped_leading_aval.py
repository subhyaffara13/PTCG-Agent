
def unmapped_leading_aval(size, aval) -> AbstractValue:
  return unmapped_aval(size, aval.leading_axis_spec(), aval)

