
def _ConsumeUint32(tokenizer):
  """Consumes an unsigned 32bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an unsigned 32bit integer couldn't be consumed.
  """
  return _ConsumeInteger(tokenizer, is_signed=False, is_long=False)

