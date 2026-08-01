
def _quote_long_string(s: str | bytes | bytearray) -> str:
  """Quotes a potentially multi-line string to make the start and end obvious.

  Args:
    s: A string.

  Returns:
    The quoted string.
  """
  if isinstance(s, (bytes, bytearray)):
    try:
      s = s.decode('utf-8')
    except UnicodeDecodeError:
      s = str(s)
  return ('8<-----------\n' +
          s + '\n' +
          '----------->8\n')

