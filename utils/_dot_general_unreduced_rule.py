
def _dot_general_unreduced_rule(lhs, rhs, dimension_numbers, out_sharding):
  if getu(lhs) or getu(rhs):
    raise core.ShardingTypeError(
        f'lhs or rhs passed to dot_general cannot be unreduced. Got {lhs=} and'
        f' {rhs=}')
  if out_sharding is not None and out_sharding.spec.unreduced:  # Explicit mode
    (lhs_contracting, rhs_contracting), _ = dimension_numbers
    lhs_contracting_spec = tuple(lhs.sharding.spec.partitions[i]
                                 for i in lhs_contracting)
    rhs_contracting_spec = tuple(rhs.sharding.spec.partitions[i]
                                 for i in rhs_contracting)
    if lhs_contracting_spec != rhs_contracting_spec:
      raise core.ShardingTypeError(
          'lhs and rhs contracting dims should be sharded identically when'
          ' out_sharding provided to dot_general mentions unreduced_axes.'
          f' Got {lhs_contracting_spec=}, {rhs_contracting_spec=}')
    flat_spec = [s for s in flatten_spec(lhs_contracting_spec) if s is not None]
    if out_sharding.spec.unreduced != frozenset(flat_spec):
      raise core.ShardingTypeError(
          "out_sharding's unreduced axes should be equal to the contracting"
          f' specs. Got unreduced axes={out_sharding.spec.unreduced} and'
          f' contracting spec={lhs_contracting_spec}')
    return out_sharding.spec.unreduced
  return frozenset()

