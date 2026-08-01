
def to_linen_var(vs: variablelib.Variable) -> meta.AxisMetadata:
  metadata = vs.get_metadata()
  if 'linen_meta_type' in metadata:
    linen_type = metadata['linen_meta_type']
    if hasattr(linen_type, 'from_nnx_metadata'):
      return linen_type.from_nnx_metadata({'value': vs.get_value(), **metadata})
    return linen_type(vs.get_value(), **metadata)
  if is_vanilla_variable(vs):
    return vs.get_value()
  return NNXMeta(type(vs), vs.get_value(), metadata)

