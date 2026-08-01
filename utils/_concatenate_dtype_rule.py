
def _concatenate_dtype_rule(*operands, **kwargs):
  check_same_dtypes('concatenate', *operands)
  return operands[0].dtype

