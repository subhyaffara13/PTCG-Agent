
def tmem_native_layout(vector_length: int):
  """A layout resembling the logical organization of TMEM.

  The 128 rows in a tile are assigned to 128 lanes in the warpgroup. Useful when
  the result needs to be processed in registers and then stored back into TMEM.
  Usually shouldn't be used if the result is to be written back to SMEM, as
  there is no good way to store it without bank conflicts, but it still
  sometimes pays off.
  """
  return TiledLayout(
      Tiling(((128, vector_length), (32, vector_length))),
      warp_dims=(-4,),
      lane_dims=(-2,),
      vector_dim=-1,
  )

