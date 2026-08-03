from typing import Any

def _is_full(fragments: _GenericFragments[Any]) -> bool:
  """True iff every array element is covered by some fragment."""
  present = np.zeros(fragments.shape, dtype=bool)
  for f in fragments.fragments:
    present[f.index] = True
  return np.all(present)

