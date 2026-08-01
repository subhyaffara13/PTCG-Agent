
def _reduce_chooser_jvp_rule(g, ans, operand, *, axes):
  # TODO(mattjj): an alternative is to use variadic reduce to compute the chosen
  # locations in a single pass (rather than comparing equality) and use a
  # gather, and/or even push along the chosen elements of g (b/112040122)
  shape = [1 if i in axes else d for i, d in enumerate(operand.shape)]
  location_indicators = convert_element_type(
      _eq_meet(operand, reshape(ans, shape)), g.dtype)
  counts = reduce_sum(location_indicators, axes)
  return div(reduce_sum(mul(g, location_indicators), axes), counts)

