
def CUnescape(text: str) -> bytes:
  """Unescape a text string with C-style escape sequences to UTF-8 bytes.

  Args:
    text: The data to parse in a str.
  Returns:
    A byte string.
  """

  def ReplaceHex(m):
    # Only replace the match if the number of leading back slashes is odd. i.e.
    # the slash itself is not escaped.
    if len(m.group(1)) & 1:
      return m.group(1) + 'x0' + m.group(2)
    return m.group(0)

  # This is required because the 'string_escape' encoding doesn't
  # allow single-digit hex escapes (like '\xf').
  result = _CUNESCAPE_HEX.sub(ReplaceHex, text)

  # Replaces Unicode escape sequences with their character equivalents.
  result = result.encode('raw_unicode_escape').decode('raw_unicode_escape')
  # Encode Unicode characters as UTF-8, then decode to Latin-1 escaping
  # unprintable characters.
  result = result.encode('utf-8').decode('unicode_escape')
  # Convert Latin-1 text back to a byte string (latin-1 codec also works here).
  return result.encode('latin-1')

