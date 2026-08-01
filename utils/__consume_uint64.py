
def _ConsumeUint64(tokenizer):
  """Consumes an unsigned 64bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an unsigned 64bit integer couldn't be consumed.
  """
  return _ConsumeInteger(tokenizer, is_signed=False, is_long=True)

