
def _tile_to_size(arr: Array, size: int) -> Array:
  assert arr.ndim == 1
  if arr.size < size:
    arr = tile(arr, int(np.ceil(size / arr.size)))
  assert arr.size >= size
  return arr[:size] if arr.size > size else arr

