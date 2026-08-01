
def _to_tiled_layout_attr(
    layout: fa.TiledLayout,
) -> mgpu.TiledLayoutAttr:
  """Constructs a #mosaic_gpu.TiledLayout attribute from a TiledLayout."""
  i64 = ir.IntegerType.get_signless(64)

  def _int_or_replicated(d: int | fa.Replicated) -> ir.Attribute:
    if isinstance(d, fa.Replicated):
      return mgpu.ReplicatedAttr.get(d.times)
    return ir.IntegerAttr.get(i64, d)

  def _tile_attr(tile):
    return ir.ArrayAttr.get([ir.IntegerAttr.get(i64, d) for d in tile])

  tiling_attr = ir.ArrayAttr.get(
      [_tile_attr(tile) for tile in layout.tiling.tiles]
  )
  warp_dims_attr = ir.ArrayAttr.get(
      [_int_or_replicated(d) for d in layout.warp_dims]
  )
  lane_dims_attr = ir.ArrayAttr.get(
      [_int_or_replicated(d) for d in layout.lane_dims]
  )

  return mgpu.TiledLayoutAttr.get(
      tiling_attr, warp_dims_attr, lane_dims_attr, layout.vector_dim
  )

