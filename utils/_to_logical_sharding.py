
def _to_logical_sharding(
    aval: core.AbstractValue, sharding: MaybeSharding
) -> JSharding | None:
  if isinstance(sharding, UnspecifiedValue):
    return None
  elif isinstance(aval, (ShapedArray, AbstractRef)):
    assert isinstance(sharding, JSharding)
    return sharding
  elif isinstance(aval, core.AbstractToken):
    return None
  else:
    raise TypeError(aval)

