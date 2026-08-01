
def override_empty_value_typestr(
    typestr: str, pytree_metadata_options: PyTreeMetadataOptions
) -> str:
  """Returns updated typestr based on pytree_metadata_options."""
  if not pytree_metadata_options.support_rich_types:
    if typestr == RESTORE_TYPE_NAMED_TUPLE:
      return RESTORE_TYPE_NONE
  return typestr

