
def _StrConvert(value):
  """Converts value to str if it is not."""
  # This file is imported by c extension and some methods like ClearField
  # requires string for the field name. py2/py3 has different text
  # type and may use unicode.
  if not isinstance(value, str):
    return value.encode('utf-8')
  return value

