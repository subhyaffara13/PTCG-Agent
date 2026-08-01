
def _cumred_sharding_rule(x, *, axis: int, reverse: bool):
  if x.sharding.spec[axis] is not None:
    raise core.ShardingTypeError(
        'Input should be unsharded over the axis being reduced. Got input'
        f' type={x} and {axis=}')
  return x.sharding

