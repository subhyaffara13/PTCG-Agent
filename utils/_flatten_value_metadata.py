
def _flatten_value_metadata(
  value_metadata: tp.Union[tp.Any, ValueMetadata],
):
  metadata = tuple(sorted(value_metadata.metadata.items()))
  return (value_metadata.value,), (value_metadata.var_type, metadata)

