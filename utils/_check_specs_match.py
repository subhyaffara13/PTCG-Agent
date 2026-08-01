
def _check_specs_match(lhs_spec, rhs_spec, msg):
  for l, r in zip(lhs_spec, rhs_spec):
    if l is not None and r is not None and l != r:
      raise core.ShardingTypeError(msg)

