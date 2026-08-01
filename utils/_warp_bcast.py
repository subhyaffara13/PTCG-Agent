
def _warp_bcast(val, lane_idx=0):
  i32 = ir.IntegerType.get_signless(32)
  mask = c(0xFFFFFFFF, i32)
  return nvvm_shfl_sync(
      val.type, mask, val, c(lane_idx, i32), c(0x1F, i32), nvvm.ShflKind.idx
  )

