
def _unpack_i32(vec_ty, r):
  i32 = ir.IntegerType.get_signless(32)
  return vector.bitcast(
      vec_ty, vector.broadcast(ir.VectorType.get((1,), i32), r)
  )

