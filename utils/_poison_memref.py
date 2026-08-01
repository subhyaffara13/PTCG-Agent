
def _poison_memref(ref: ir.Value):
  memref_type = ref.type
  elem_type = memref_type.element_type

  if isinstance(elem_type, ir.FloatType):
    poison_val = ir_constant(float("nan"), elem_type)
  elif isinstance(elem_type, ir.IntegerType):
    width = elem_type.width
    if width == 1:
      poison_val = ir_constant(True, elem_type)
    else:
      poison_val = ir_constant(-(1 << (width - 1)), elem_type)
  else:
    raise NotImplementedError(
        f"Unsupported element type for poisoning: {elem_type}"
    )

  shape = memref_type.shape
  if not shape:
    memref.store(poison_val, ref, [])
    return

  vector_type = ir.VectorType.get(shape, elem_type)
  poison_vec = vector.broadcast(vector_type, poison_val)

  index_type = ir.IndexType.get()
  zero = arith.constant(index_type, 0)
  indices = [zero] * len(shape)
  vector.store(poison_vec, ref, indices)

