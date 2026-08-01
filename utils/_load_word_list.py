
def _load_word_list(word_list_file: str):
  """Returns the word dict."""
  # Get the content of the named resource as a string.
  contents = pyspiel.read_contents_from_file(word_list_file, "r")
  lines = contents.split("\n")
  word_list = []
  max_word_length = 0
  for line in lines:
    if not line:
      continue
    line_len = len(line)
    if _is_valid_word(line):
      word_list.append(line)
      max_word_length = max(max_word_length, line_len)
  assert word_list
  return word_list, max_word_length

