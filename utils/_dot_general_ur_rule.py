
def _dot_general_ur_rule(lhs, rhs, *, dimension_numbers, out_sharding, **kwargs):
  out_unreduced = _dot_general_unreduced_rule(lhs, rhs, dimension_numbers,
                                              out_sharding)
  # TODO(yashkatariya): Propagate reduced and make checks like nary_reduced_rule
  return out_unreduced, frozenset()

