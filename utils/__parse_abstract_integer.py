
def _ParseAbstractInteger(text):
  """Parses an integer without checking size/signedness.

  Args:
    text: The text to parse.

  Returns:
    The integer value.

  Raises:
    ValueError: Thrown Iff the text is not a valid integer.
  """
  # Do the actual parsing. Exception handling is propagated to caller.
  orig_text = text
  c_octal_match = re.match(r'(-?)0(\d+)$', text)
  if c_octal_match:
    # Python 3 no longer supports 0755 octal syntax without the 'o', so
    # we always use the '0o' prefix for multi-digit numbers starting with 0.
    text = c_octal_match.group(1) + '0o' + c_octal_match.group(2)
  try:
    return int(text, 0)
  except ValueError:
    raise ValueError('Couldn\'t parse integer: %s' % orig_text)

