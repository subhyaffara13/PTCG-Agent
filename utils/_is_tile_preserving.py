
def _is_tile_preserving(
    shape: tuple[int, ...],
    transforms: Sequence[Transform],
    tiling: tuple[int, int] | None = None,
) -> bool:
  if not tiling or len(shape) < 2:
    return False

  t1, t2 = tiling
  if shape[-2] % t1 != 0 or shape[-1] % t2 != 0:
    return False

  dims = _init_dims(shape, t1, t2)

  for t in transforms:
    match t:
      case SplitDims(index, sizes):
        if (new_dims := _apply_split(dims[index], sizes)) is None:
          return False
        dims[index : index + 1] = new_dims
      case MergeDims(index, count):
        merged = [b for d in dims[index : index + count] for b in d]
        dims[index : index + count] = [_consolidate(merged)]
      case Transpose(permutation):
        dims = [dims[i] for i in permutation]

  if len(dims) < 2:
    return False

  # Check that the last two dimensions are tiled along (sublane, lane).
  y_dim = dims[-2]
  if not y_dim or y_dim[-1] != Factor(t1, "sublane"):
    return False

  x_dim = dims[-1]
  if not x_dim or x_dim[-1] != Factor(t2, "lane"):
    return False

  return True

