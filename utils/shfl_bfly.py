
def shfl_bfly(x: ir.Value, distance: int | ir.Value):
  i32 = ir.IntegerType.get_signless(32)
  if isinstance(distance, int):
    distance = c(distance, i32)
  if (result_type := x.type) != i32:
    if (x_bitwidth := bitwidth(x.type)) < 32:  # Pad to 32-bits if necessary.
      assert 32 % x_bitwidth == 0
      x = bitcast(x, ir.IntegerType.get_signless(x_bitwidth))
      empty32 = llvm.mlir_undef(ir.VectorType.get((32 // x_bitwidth,), x.type))
      x = vector.insert(
          x,
          empty32,
          dynamic_position=[],
          static_position=ir.DenseI64ArrayAttr.get([0]),
      )
    elif x_bitwidth > 32:
      assert x_bitwidth % 32 == 0
      num_words = x_bitwidth // 32
      xs_vec = bitcast(x, ir.VectorType.get((num_words,), i32))
      y = llvm.mlir_undef(xs_vec.type)
      for i in range(num_words):
        x_elem = vector.extract(
            xs_vec,
            dynamic_position=[],
            static_position=ir.DenseI64ArrayAttr.get([i]),
        )
        y_elem = shfl_bfly(x_elem, distance)
        y = vector.insert(
            y_elem,
            y,
            dynamic_position=[],
            static_position=ir.DenseI64ArrayAttr.get([i]),
        )
      return bitcast(y, result_type)
    x = bitcast(x, i32)
  y = nvvm_shfl_sync(
      i32,
      c(0xFFFFFFFF, i32),
      x,
      distance,
      c(0x1F, i32),
      nvvm.ShflKind.bfly
  )
  if (x_bitwidth := bitwidth(result_type)) < 32:
    bits_ty = ir.IntegerType.get_signless(x_bitwidth)
    y_vec = bitcast(y, ir.VectorType.get((32 // x_bitwidth,), bits_ty))
    y = vector.extract(
        y_vec,
        dynamic_position=[],
        static_position=ir.DenseI64ArrayAttr.get([0]),
    )
  return bitcast(y, result_type)

