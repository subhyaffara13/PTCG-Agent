
def retrieve_alpha_block(text: str) -> str:
  """Return the first instance of a contiguous alpha(not numeric) substring."""
  first_alpha_char = next(filter(str.isalpha, text), -1)
  if first_alpha_char == -1:
    return ''
  start = text.find(first_alpha_char)
  sliced = text[start:]
  last_alpha_char = next(filter(lambda s: not str.isalpha(s), sliced), -1)
  if last_alpha_char == -1:
    return sliced
  finish = sliced.find(last_alpha_char)
  return text[start:start + finish]

