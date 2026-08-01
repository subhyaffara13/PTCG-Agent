
def _TryConsumeInt64(tokenizer):
  try:
    _ConsumeInt64(tokenizer)
    return True
  except ParseError:
    return False

