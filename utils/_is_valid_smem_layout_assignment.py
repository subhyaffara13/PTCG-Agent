
def _is_valid_smem_layout_assignment(
    shape: tuple[int, ...], tiling: lc.TileTransform
) -> bool:
  try:
    # `tiling.transform_shape` will raise if the shape is not tileable.
    _ = tiling.transform_shape(shape)
  except ValueError:
    return False
  return True

