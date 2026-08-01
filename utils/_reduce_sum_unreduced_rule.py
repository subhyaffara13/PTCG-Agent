
def _reduce_sum_unreduced_rule(operand, axes, out_sharding):
  if out_sharding is not None and out_sharding.spec.unreduced:  # explicit mode
    axes = frozenset(axes)
    used_spec = frozenset(
        s for i, spec in enumerate(operand.sharding.spec.partitions)
        if i in axes for s in (spec if isinstance(spec, tuple) else (spec,))
    ) | operand.sharding.spec.unreduced
    if not all(u in used_spec for u in out_sharding.spec.unreduced):
      raise core.ShardingTypeError(
          "out_sharding's unreduced axes should be in operand's specs that"
          f' were summed over. Got {operand=}, {axes=},'
          f' unreduced_spec={out_sharding.spec.unreduced}')
    return out_sharding.spec.unreduced
  return getu(operand)

