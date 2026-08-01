
def mask_at(t: tuple, index: int | None) -> tuple:
  if index is None:
    return t
  return tuple(
    Mask() if i == index else x
    for i, x in enumerate(t)
  )

