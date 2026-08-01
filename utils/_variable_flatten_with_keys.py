
def _variable_flatten_with_keys(x: Variable[tp.Any]):
  metadata = tuple(sorted(x._var_metadata.items()))
  node = (jtu.GetAttrKey('value'), x._raw_value)
  return (node,), metadata

