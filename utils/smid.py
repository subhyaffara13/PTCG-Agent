
def smid():
  i32 = ir.IntegerType.get_signless(32)
  return llvm.inline_asm(i32, [], "mov.u32  $0,%smid;", "=r", asm_dialect=0)

