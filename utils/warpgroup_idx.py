
def warpgroup_idx(sync=True):
  i32 = ir.IntegerType.get_signless(32)
  wg_idx = arith.shrui(thread_idx(), c(7, i32))
  # Performing a warp broadcast improves performance as compiler understands
  # that the value is uniform across the warp.
  return _warp_bcast(wg_idx) if sync else wg_idx

