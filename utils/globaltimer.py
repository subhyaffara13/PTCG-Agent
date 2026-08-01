
def globaltimer(kind: Literal["low", "high"] | None = None):
  if kind is None:
    i64 = ir.IntegerType.get_signless(64)
    return llvm.inline_asm(
        i64,
        [],
        "mov.u64  $0,%globaltimer;",
        "=l",
        asm_dialect=0,
        has_side_effects=True,
    )
  i32 = ir.IntegerType.get_signless(32)
  return llvm.inline_asm(
      i32,
      [],
      f"mov.u32  $0,%globaltimer_{kind[:2]};",
      "=r",
      asm_dialect=0,
      has_side_effects=True,
  )

