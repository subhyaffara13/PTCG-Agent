
def _reduce_sum_sharding_rule(operand, *, axes, out_sharding):
  if out_sharding is not None:
    assert isinstance(out_sharding, NamedSharding)
    return out_sharding
  axes = frozenset(axes)
  new_spec = P(*tuple(s for i, s in enumerate(operand.sharding.spec.partitions)
                      if i not in axes))
  return operand.sharding.update(spec=new_spec)

