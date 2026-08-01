
def _reduce_weak_type_rule(*avals, computation, jaxpr, dimensions):
  operand_avals, init_val_avals = split_list(avals, [len(avals) // 2])
  return [op.weak_type and init_val.weak_type
          for op, init_val in safe_zip(operand_avals, init_val_avals)]

