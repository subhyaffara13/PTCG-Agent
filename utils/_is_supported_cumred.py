
def _is_supported_cumred(inp, axis, reverse):
  return False
  return (
      jaxlib_extension_version >= 460
      and not reverse
      and isinstance(inp, ShapedArray)
      and core.is_constant_shape(inp.shape)
      and inp.shape[axis] > 0
      and inp.sharding.spec[axis] is None
      and inp.dtype != np.bool_
      and not np.issubdtype(inp.dtype, np.complexfloating)
  )

