
def _stack_dtype_rule(*operands, axis):
  check_same_dtypes('stack', *operands)
  return operands[0].dtype

