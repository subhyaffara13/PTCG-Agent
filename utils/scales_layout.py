
def scales_layout() -> TMEMLayout:
  """A TMEM layout for A and B scales in .scale_vec::1X configuration.

  See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-mma-scale-factor-a-layout-1x
  """
  TMEM_QUARTER = TMEM_ROWS // 4
  # Note that the * 4 after TMEM_QUARTER applies logically to rows, but it's
  # split across 4 consecutive columns, not across the 4 quarters of TMEM.
  return TMEMLayout(
      fa.Tiling(((TMEM_QUARTER * 4, 4), (TMEM_QUARTER, 1))),
      warp_dims=(fa.Replicated(times=4),),
      lane_dims=(-2,),
      vector_dim=-3,
  )

