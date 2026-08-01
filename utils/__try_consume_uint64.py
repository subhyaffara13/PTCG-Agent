
def _TryConsumeUint64(tokenizer):
  try:
    _ConsumeUint64(tokenizer)
    return True
  except ParseError:
    return False

