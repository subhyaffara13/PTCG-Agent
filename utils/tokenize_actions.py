
def tokenize_actions(street_text: str) -> tuple[tuple[str, int | None], ...]:
  """Return tokens as ('c', None), ('f', None), ('r', amount).

  Args:
    street_text: The string representing actions on a single street.

  Raises ValueError with position info on invalid input.
  """
  if not street_text:
    return tuple()
  tokens = _token_re.findall(street_text)
  if "".join(tokens) != street_text:
    # find first bad position
    i = 0
    j = 0
    while i < len(street_text) and j < len(tokens):
      t = tokens[j]
      if street_text.startswith(t, i):
        i += len(t)
        j += 1
      else:
        break
    raise ValueError(f"Invalid action string at pos {i} in {street_text!r}")
  parsed: list[tuple[str, int | None]] = []
  k = 0
  while k < len(street_text):
    ch = street_text[k]
    if ch in ("c", "f"):
      parsed.append((ch, None))
      k += 1
    elif ch == "r":
      k += 1
      start = k
      while k < len(street_text) and street_text[k].isdigit():
        k += 1
      if k == start:
        raise ValueError(
            f"raise without amount at pos {start} in {street_text!r}"
        )
      amt = int(street_text[start:k])
      parsed.append(("r", amt))
    else:
      raise ValueError(f"invalid char {ch!r} at pos {k} in {street_text!r}")
  return tuple(parsed)

