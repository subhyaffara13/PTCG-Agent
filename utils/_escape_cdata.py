
def _escape_cdata(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s


def _escape_cdata(s):
  """Escapes a string to be used as XML CDATA.

  CDATA characters are treated strictly as character data, not as XML markup,
  but there are still certain restrictions on them.

  Args:
    s: the string to be escaped.
  Returns:
    An escaped version of the input string.
  """
  for char, escaped in _control_character_conversions.items():
    s = s.replace(char, escaped)
  return s.replace(']]>', ']] >')

