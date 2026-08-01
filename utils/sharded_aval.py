
def sharded_aval(aval: core.AbstractValue,
                 sharding: JSharding | None) -> core.AbstractValue:
  """Returns the new aval sharded based on sharding proto."""
  if sharding is None:
    return aval
  if isinstance(aval, core.AbstractToken):
    return aval
  if not isinstance(aval, core.ShapedArray):
    raise NotImplementedError
  return aval.update(sharding.shard_shape(aval.shape), sharding=None)

