
def _ConsumeInt64(tokenizer):
  """Consumes a signed 32bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If a signed 32bit integer couldn't be consumed.
  """
  return _ConsumeInteger(tokenizer, is_signed=True, is_long=True)

