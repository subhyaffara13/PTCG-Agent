
def nnx_attrs_to_linen_vars(nnx_attrs: dict) -> dict:
  """Convert a dict of NNX variables to Linen-style variables."""
  linen_structured = {}
  for kp, v in traversals.flatten_mapping(nnx_attrs).items():
    if isinstance(v, variablelib.Variable):
      col_name = variablelib.variable_name_from_type(type(v))
      v = to_linen_var(v.to_state())
    else:
      raise ValueError(f'Cannot infer collection name from value: {v}')
    linen_structured[(col_name, *kp)] = v
  variables = traversals.unflatten_mapping(linen_structured)
  return variables

