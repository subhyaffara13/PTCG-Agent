
def _ConvertBool(value, require_str):
  """Convert a boolean value.

  Args:
    value: A scalar value to convert.
    require_str: If True, value must be a str.

  Returns:
    The bool parsed.

  Raises:
    ParseError: If a boolean value couldn't be consumed.
  """
  if require_str:
    if value == 'true':
      return True
    elif value == 'false':
      return False
    else:
      raise ParseError('Expected "true" or "false", not {0}'.format(value))

  if not isinstance(value, bool):
    raise ParseError('Expected true or false without quotes')
  return value

