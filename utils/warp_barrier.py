
def warp_barrier():
  nvvm.bar_warp_sync(c(0xFFFFFFFF, ir.IntegerType.get_signless(32)))

