
def fa_m64_collective_layout(columns: int) -> fa.TiledLayout:
  """The register layout for transfers to/from tmem_m64_collective_layout."""
  if columns % 16:
    raise ValueError(f"Columns must be a multiple of 16, got: {columns}")
  return fa.TiledLayout(
      fa.Tiling((
          (TMEM_ROWS // 2, columns), (fa.WARP_SIZE, columns // 2), (8, 8), (2,)
      )),
      warp_dims=(-6, -7),
      lane_dims=(-3, -2),
      vector_dim=-1,
  )

