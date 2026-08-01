
def clock():
  i32 = ir.IntegerType.get_signless(32)
  return llvm.inline_asm(
      i32, [], "mov.u32  $0,%clock;", "=r", asm_dialect=0, has_side_effects=True
  )

