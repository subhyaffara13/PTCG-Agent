
def warp_idx(sync=True):
  i32 = ir.IntegerType.get_signless(32)
  warp_idx = arith.shrui(thread_idx(), c(5, i32))
  # Performing a warp broadcast improves performance as compiler understands
  # that the value is uniform across the warp.
  return _warp_bcast(warp_idx) if sync else warp_idx

