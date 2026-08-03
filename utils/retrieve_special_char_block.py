from typing import Tuple

def retrieve_special_char_block(text: str,
                                special_chars: Tuple[str, ...] = ('*',),
                                useless_chars: Tuple[str, ...] = (' ', '\n')):
  for char in special_chars:
    text = text.strip(char)
  idx_end = first_special_char(text, len(text), special_chars)
  text = text[:idx_end]
  for char in useless_chars:
    text = text.strip(char)
  return text

