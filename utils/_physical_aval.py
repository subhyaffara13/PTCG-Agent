
def _physical_aval(aval):
  if isinstance(aval, core.ShapedArray):
    if isinstance(aval.dtype, FusionDType):
      return aval.dtype.abstract_unpack(aval)
    return core.ShapedArray(aval.shape, aval.dtype)
  if isinstance(aval, state.AbstractRef):
    if _is_fusion_type(aval):
      unpacked = aval.dtype.abstract_unpack(aval.inner_aval)
      return tuple(aval.update(inner_aval=u) for u in unpacked)
    return aval
  return aval


def _physical_aval(aval: ShapedAbstractValue) -> ShapedAbstractValue:
  assert isinstance(aval, jax_core.AbstractValue)
  return cast(ShapedAbstractValue, jax_core.physical_aval(aval))

