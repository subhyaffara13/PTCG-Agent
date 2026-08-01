
def _from_tiled_layout_attr(
    attr: mgpu.TiledLayoutAttr,
) -> fa.TiledLayout:
  """Constructs a TiledLayout from a #mosaic_gpu.TiledLayout attribute."""

  def _from_int_or_replicated_attr(d_attr: ir.Attribute) -> int | fa.Replicated:
    if isinstance(d_attr, mgpu.ReplicatedAttr):
      return fa.Replicated(times=mgpu.ReplicatedAttr(d_attr).times)
    return ir.IntegerAttr(d_attr).value

  tiles = tuple(
      tuple(ir.IntegerAttr(d).value for d in ir.ArrayAttr(tile))
      for tile in attr.tiling
  )
  warp_dims = tuple(_from_int_or_replicated_attr(d) for d in attr.warp_dims)
  lane_dims = tuple(_from_int_or_replicated_attr(d) for d in attr.lane_dims)

  return fa.TiledLayout(
      tiling=fa.Tiling(tiles),
      warp_dims=warp_dims,
      lane_dims=lane_dims,
      vector_dim=attr.vector_dim,
  )

