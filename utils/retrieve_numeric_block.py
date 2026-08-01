
def retrieve_numeric_block(text: str) -> str:
  """Return the first instance of a contiguous numeric(not alpha) substring."""
  first_numeric_char = next(filter(str.isnumeric, text), -1)
  if first_numeric_char == -1:
    return ''
  start = text.find(first_numeric_char)
  sliced = text[start:]
  last_numeric_char = next(filter(lambda s: not str.isnumeric(s), sliced), -1)
  if start > 0 and text[start - 1] == '-':
    start -= 1
    sliced = text[start:]
  if last_numeric_char == -1:
    return sliced
  finish = sliced.find(last_numeric_char)
  return text[start:start + finish]

