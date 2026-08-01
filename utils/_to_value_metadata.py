
def _to_value_metadata(node):
  def to_value_metadata(x):
    if isinstance(x, variablelib.Variable):
      value = x.get_raw_value()
      if variablelib.is_array_ref(value):
        value = value[...]
      metadata = x.get_metadata()
      return ValueMetadata(var_type=x.var_type, value=value, metadata=metadata)
    return x

  return jax.tree.map(
    to_value_metadata,
    node,
    is_leaf=lambda x: isinstance(x, variablelib.Variable),
  )

