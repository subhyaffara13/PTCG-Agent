
def to_layout_attr(layout: fa.FragmentedLayout) -> ir.Attribute:
  """Constructs an MLIR attribute that corresponds to the given layout."""
  match layout:
    case fa.WGSplatFragLayout():
      return _to_splat_fragmented_layout_attr(layout)
    case fa.WGStridedFragLayout():
      return _to_strided_fragmented_layout_attr(layout)
    case fa.TiledLayout():
      return _to_tiled_layout_attr(layout)
    case _:
      assert_never(layout)

