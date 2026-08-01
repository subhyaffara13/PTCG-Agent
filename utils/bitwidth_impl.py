
def bitwidth_impl(ty: ir.Type):
  # The actual width of TF32 is 19 bits. However, we need to treat it as
  # 32 bits for compatibility reasons. TF32 used to be 32 bits wide in upstream
  # MLIR, but it changed in
  # https://github.com/llvm/llvm-project/commit/67a1fdb014790a38a205d28e1748634de34471dd.
  if isinstance(ty, ir.FloatTF32Type):
    return 32
  if isinstance(ty, ir.IntegerType):
    return ir.IntegerType(ty).width
  if isinstance(ty, ir.FloatType):
    return ir.FloatType(ty).width
  if dialect is not None and isinstance(ty, dialect.BarrierType):
    return MBARRIER_BYTES * 8
  if isinstance(ty, ir.VectorType):
    vty = ir.VectorType(ty)
    return math.prod(vty.shape) * bitwidth(vty.element_type)
  raise NotImplementedError(ty)

