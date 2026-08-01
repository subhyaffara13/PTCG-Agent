
def _unflatten_value_metadata(aux_data, children):
  var_type, metadata_items = aux_data
  metadata = dict(metadata_items)
  return ValueMetadata(var_type=var_type, value=children[0], metadata=metadata)

