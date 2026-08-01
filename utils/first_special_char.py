
def first_special_char(text: str,
                       max_idx: int,
                       special_chars: Tuple[str, ...]) -> int:
  first_special_chars = [max_idx]
  for char in special_chars:
    idx = text.find(char)
    if idx < 0:
      first_special_chars.append(max_idx)
    else:
      first_special_chars.append(idx)
  return min(first_special_chars)

