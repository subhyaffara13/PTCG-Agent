
def b_scales_m64_collective_layout() -> TMEMLayout:
  """A TMEM layout for B scales in 2CTA M=128 (.scale_vec::1X) configuration.

  When M per CTA is 64, the B scales use a different TMEM addressing than the
  standard scales_layout(). The first half of the data is in quarters 0 and 2,
  while the second half goes to quarters 1 and 3.
  """
  TMEM_QUARTER = TMEM_ROWS // 4
  return TMEMLayout(
      fa.Tiling(((TMEM_ROWS * 2, 4), (TMEM_ROWS, 4), (TMEM_QUARTER, 4))),
      warp_dims=(fa.Replicated(times=2), -6),
      lane_dims=(-2,),
      vector_dim=-1,
  )

