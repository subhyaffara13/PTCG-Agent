
def _normalize_shape_item(item: _ShapeItem) -> ShapeSpec:
  """Returns the `str` representation associated with the shape element."""
  if isinstance(item, str):
    return item
  elif isinstance(item, int):
    return str(item)
  elif isinstance(item, _EllipsisType):
    return '...'
  elif item is None:
    return '_'
  else:
    raise TypeError(f'Invalid shape type {type(item)} of: {item}')

