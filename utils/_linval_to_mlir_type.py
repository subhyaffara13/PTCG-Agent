
def _linval_to_mlir_type(a):
  color = {'vmem': 1, 'hbm': 0, None: None}[a.memory_space]
  space = mlir.i32_attr(color) if color is not None else None
  return mlir.ir.MemRefType.get(a.shape, mlir.dtype_to_ir_type(a.dtype),
                                memory_space=space)

