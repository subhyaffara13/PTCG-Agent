from typing import Any

def redux(x: ir.Value, mask: ir.Value, kind: ReductionKind):
  i32 = ir.IntegerType.get_signless(32)
  if isinstance(vec_ty := x.type, ir.VectorType):
    if bitwidth(vec_ty.element_type) != 32:
      raise ValueError("Only 32-bit types supported")
    [vec_len] = vec_ty.shape
    result = llvm.mlir_undef(x.type)
    for i in range(vec_len):
      xi = llvm.extractelement(x, arith.constant(i32, i))
      yi = redux(xi, mask, kind)
      result = llvm.insertelement(result, yi, arith.constant(i32, i))
    return result
  if bitwidth(x.type) != 32:
    raise ValueError("Only 32-bit scalar types supported")
  if isinstance(x.type, ir.IntegerType):
    pass
  elif isinstance(x.type, ir.F32Type):
    if get_arch().major != 10:
      raise ValueError("F32 redux only supported on Blackwell GPUs")
  else:
    raise NotImplementedError(x.type)
  assert mask.type == i32
  extra_kwargs: dict[str, Any] = {}
  if kind == ReductionKind.FMAX or kind == ReductionKind.FMIN:
    extra_kwargs = dict(nan=True)
  return nvvm.redux_sync(x, kind, mask, **extra_kwargs)

