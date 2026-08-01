
def _variable_flatten(x: Variable[tp.Any]):
  metadata = tuple(sorted(x._var_metadata.items()))
  return (x._raw_value,), metadata

