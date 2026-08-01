
def _is_valid_word(word: str):
  if len(word) < _MIN_WORD_LENGTH:
    return False
  for l in word:
    if l not in _VALID_LETTERS and l not in _SKIP_LETTERS:
      return False
  return True

