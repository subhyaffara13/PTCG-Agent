
def _ConsumeInteger(tokenizer, is_signed=False, is_long=False):
  """Consumes an integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.
    is_signed: True if a signed integer must be parsed.
    is_long: True if a long integer must be parsed.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an integer with given characteristics couldn't be consumed.
  """
  try:
    result = ParseInteger(tokenizer.token, is_signed=is_signed, is_long=is_long)
  except ValueError as e:
    raise tokenizer.ParseError(str(e))
  tokenizer.NextToken()
  return result

