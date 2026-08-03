from typing import Optional

def _get_item_or_attribute(config, field,
                           field_path: Optional[str] = None):
  """Returns attribute of member failing that the item."""
  if isinstance(field, str) and hasattr(config, field):
    return getattr(config, field)
  if hasattr(config, '__getitem__'):
    return config[field]
  if isinstance(field, int):
    raise IndexError(
        f'{type(config)} does not support integer indexing [{field}]]. '
        f'Attempting to lookup: {field_path}')
  raise KeyError(
      f'Attribute {type(config)}.{field} does not exist '
      'and the type does not support indexing. '
      f'Attempting to lookup: {field_path}')

