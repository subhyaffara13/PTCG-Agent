
def get_empty_value_typestr(
    value: Any, pytree_metadata_options: PyTreeMetadataOptions
) -> str:
  """Returns the typestr constant for the empty value."""
  if not is_supported_empty_value(value, pytree_metadata_options):
    raise ValueError(
        f'{value} is not a supported empty type with pytree_metadata_options:'
        f' {pytree_metadata_options}.'
    )
  if isinstance(value, list):
    return RESTORE_TYPE_LIST
  if tree_utils.isinstance_of_namedtuple(value):  # Call before tuple check.
    return RESTORE_TYPE_NAMED_TUPLE
  if isinstance(value, tuple):
    return RESTORE_TYPE_TUPLE
  if isinstance(value, (dict, Mapping)):
    return RESTORE_TYPE_DICT
  if value is None:
    return RESTORE_TYPE_NONE
  raise ValueError(
      f'Unrecognized empty type: {value} with pytree_metadata_options:'
      f' {pytree_metadata_options}.'
  )

