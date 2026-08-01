
def _infer_reduce_op_return_types(
    operands: Sequence[ir.Value], axis: int
) -> Sequence[ir.Type]:
  return_types = []
  for op in operands:
    op_type = ir.RankedTensorType(op.type)
    shape = list(op_type.shape)
    del shape[axis]
    if not shape:
      return_types.append(op_type.element_type)
    elif op_encoding := op_type.encoding:
      encoding = _infer_reduce_op_encoding(op_encoding, axis)
      if encoding is not None:
        raise RuntimeError("Failed to infer return type encoding for ReduceOp")
      return_types.append(
          ir.RankedTensorType.get(shape, op_type.element_type, encoding)
      )
    else:
      return_types.append(ir.RankedTensorType.get(shape, op_type.element_type))
  return return_types

