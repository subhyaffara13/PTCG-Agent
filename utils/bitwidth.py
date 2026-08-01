
def bitwidth(ty: ir.Type):
  result = bitwidth_impl(ty)
  if result.bit_count() != 1:
    raise ValueError(f"Only power of 2 bitwidths are supported, got: {result}")
  return result

