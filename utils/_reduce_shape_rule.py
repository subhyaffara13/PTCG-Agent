
def _reduce_shape_rule(*avals, computation, jaxpr, dimensions):
  operand_avals, init_val_avals = split_list(avals, [len(avals) // 2])
  if any(arg.shape != () for arg in init_val_avals):
    init_val_shapes = [a.shape for a in init_val_avals]
    raise ValueError(f'reduce found non-scalar initial value: {init_val_shapes}')
  return [tuple(np.delete(op.shape, dimensions)) for op in operand_avals]

