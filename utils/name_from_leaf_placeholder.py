
def name_from_leaf_placeholder(placeholder: str) -> str:
  """Gets the param name from a placeholder with the correct prefix."""
  if not leaf_is_placeholder(placeholder):
    msg = (
        'Requested name from placeholder, but value did not contain required'
        ' prefix.'
    )
    raise ValueError(msg)
  if placeholder.startswith(_AGGREGATED_PREFIX):
    return placeholder.replace(_AGGREGATED_PREFIX, '', 1)
  elif placeholder.startswith(_PLACEHOLDER_PREFIX):
    return placeholder.replace(_PLACEHOLDER_PREFIX, '', 1)
  else:
    raise ValueError('Found placeholder beginning with unexpected prefix.')

