
def bytewidth(ty: ir.Type):
  bw = bitwidth(ty)
  assert bw % 8 == 0, ty
  return bw // 8

