
def mapped_leading_aval(size, aval) -> AbstractValue:
  return mapped_aval(size, aval.leading_axis_spec(), aval)

