
def _is_valid_register_layout_assignment(
    shape: tuple[int, ...], layout: fa.FragmentedLayout
) -> bool:
  match layout:
    case fa.WGStridedFragLayout() as strided_layout:
      return strided_layout.shape == shape
    case fa.WGSplatFragLayout() as splat_layout:
      return splat_layout.shape == shape
    case fa.TiledLayout(tiling=tiling):
      try:
        # `tiling.tile_shape` will raise if the shape is not tileable.
        _ = tiling.tile_shape(shape)
      except ValueError:
        return False
      return True
    case _:
      assert_never(layout)

