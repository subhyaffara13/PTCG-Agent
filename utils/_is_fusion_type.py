
def _is_fusion_type(aval: core.AbstractValue):
  """Returns whether an aval is an array containing fusion types."""
  return (
      isinstance(aval, (core.ShapedArray, state.AbstractRef))
      and hasattr(aval, 'dtype')
      and isinstance(aval.dtype, FusionDType)
  )

