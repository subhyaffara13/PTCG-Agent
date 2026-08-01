
def _concatenate_reduced_rule(*operands, **kwargs):
  reduced_specs = {r for o in operands if (r := getr(o))}
  if len(reduced_specs) > 1:
    raise core.ShardingTypeError(
        'All operands should be reduced along the same mesh axes. Got reduced'
        f' specs: {reduced_specs}')
  reduced_s, = reduced_specs if reduced_specs else (frozenset(),)
  return reduced_s

