
def _merge_on_one_axis(operand, new_sizes):
  if len(new_sizes) >= len(operand.shape):
    return False, []
  return _split_on_one_axis(new_sizes, operand.shape)

