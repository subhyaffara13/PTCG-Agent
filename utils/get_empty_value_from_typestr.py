from typing import Any

def get_empty_value_from_typestr(
    typestr: str, pytree_metadata_options: PyTreeMetadataOptions
) -> Any:
  """Returns the empty value for the given typestr.

  Args:
    typestr: The typestr constant for the empty value.
    pytree_metadata_options: The pytree metadata options.

  Raises:
    ValueError: If the typestr is not supported.
  """
  if typestr == RESTORE_TYPE_LIST:
    return []
  if typestr == RESTORE_TYPE_NAMED_TUPLE:
    if pytree_metadata_options.support_rich_types:
      return OrbaxEmptyNamedTuple()
    else:
      return None
  if typestr == RESTORE_TYPE_TUPLE:
    return tuple()
  if typestr == RESTORE_TYPE_DICT:
    return {}
  if typestr == RESTORE_TYPE_NONE:
    return None
  raise ValueError(
      f'Unrecognized typestr: {typestr} with pytree_metadata_options:'
      f' {pytree_metadata_options}.'
  )

