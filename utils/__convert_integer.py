
def _ConvertInteger(value):
  """Convert an integer.

  Args:
    value: A scalar value to convert.

  Returns:
    The integer value.

  Raises:
    ParseError: If an integer couldn't be consumed.
  """
  if isinstance(value, float) and not value.is_integer():
    raise ParseError("Couldn't parse integer: {0}".format(value))

  if isinstance(value, str) and value.find(' ') != -1:
    raise ParseError('Couldn\'t parse integer: "{0}"'.format(value))

  if isinstance(value, bool):
    raise ParseError(
        'Bool value {0} is not acceptable for integer field'.format(value)
    )

  try:
    return int(value)
  except ValueError as e:
    # Attempt to parse as an integer-valued float.
    try:
      f = float(value)
    except ValueError:
      # Raise the original exception for the int parse.
      raise e  # pylint: disable=raise-missing-from
    if not f.is_integer():
      raise ParseError(
          'Couldn\'t parse non-integer string: "{0}"'.format(value)
      ) from e
    return int(f)

