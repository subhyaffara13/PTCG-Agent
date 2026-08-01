
def _concatenate_unreduced_rule(*operands, **kwargs):
  unreduced_specs = {u for o in operands if (u := getu(o))}
  if len(unreduced_specs) > 1:
    raise core.ShardingTypeError(
        'All operands should be unreduced along the same mesh axes. Got'
        f' unreduced specs: {unreduced_specs}')
  unreduced_s, = unreduced_specs if unreduced_specs else (frozenset(),)
  return unreduced_s

