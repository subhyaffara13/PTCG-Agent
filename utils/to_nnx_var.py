from typing import Any

def to_nnx_var(col: str, x: meta.AxisMetadata | Any) -> variablelib.Variable:
  """Convert a Linen variable to an NNX variable."""
  vtype = variablelib.variable_type_from_name(col, allow_register=True)
  if isinstance(x, NNXMeta):
    assert vtype == x.var_type, f'Type stored in NNXMeta {x.var_type} != type inferred from collection name {vtype}'
    return x.to_nnx_variable()
  if isinstance(x, meta.AxisMetadata):
    x_metadata = vars(x)
    if hasattr(x, 'to_nnx_metadata'):
      x_metadata = x.to_nnx_metadata()
    assert hasattr(x, 'value')
    return vtype(**x_metadata, linen_meta_type=type(x))
  return vtype(x)

