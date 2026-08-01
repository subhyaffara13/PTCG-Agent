
def _construct_serialization_param(
    value: types.Leaf,
    info: types_v0.ParamInfo,
) -> types.SerializationParam[types.Leaf]:
  assert info.keypath is not None
  return types.SerializationParam(
      keypath=info.keypath,
      value=value,
  )

