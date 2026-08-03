from typing import List

def pairs_string_to_list(positions: str) -> List[np.ndarray]:
  """Converts a string representing positions into a list of positions."""
  pos = positions[1:-1]  # remove [ and ]
  if not pos:
    return []
  split = pos.split(";")
  return [np.array([int(i) for i in s.split("|")], dtype=int) for s in split]

