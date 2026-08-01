
def _index_from_ndarray(a: NpIndex) -> Index:
  return tuple(slice(*xs) for xs in a)

