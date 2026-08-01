
def _as_i32_reg(v):
  i32 = ir.IntegerType.get_signless(32)
  return llvm.extractelement(
      vector.bitcast(ir.VectorType.get((1,), i32), v), _lc(0)
  )

