
def warpgroup_barrier():
  # gpu.barrier() uses barrier number 0, and it would be unsafe to reuse it,
  # so we shift the warpgroup index by 1.
  i32 = ir.IntegerType.get_signless(32)
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [arith.addi(warpgroup_idx(sync=False), c(1, i32))],
      f"bar.sync $0, {WARPGROUP_SIZE};",
      "r",
      has_side_effects=True,
  )

