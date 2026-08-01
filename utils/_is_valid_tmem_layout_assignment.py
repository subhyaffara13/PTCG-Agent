
def _is_valid_tmem_layout_assignment(
    shape: tuple[int, ...], layout: tcgen05.TMEMLayout
) -> bool:
  try:
    # `layout.tiling.tile_shape` will raise if the shape is not tileable.
    _ = layout.tiling.tile_shape(shape)
  except ValueError:
    return False
  return True

