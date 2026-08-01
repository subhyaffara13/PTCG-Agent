
def _dynamic_update_slice_shape_rule(operand, update, *start_indices):
  if operand.ndim != update.ndim:
    msg = ("dynamic_update_slice update must have the same rank as operand, "
           "got update shape {} for operand shape {}.")
    raise TypeError(msg.format(update.shape, operand.shape))
  if operand.ndim != len(start_indices):
    msg = ("dynamic_update_slice start_indices must have length equal to the "
           "rank of operand, got indices {} for operand shape {}.")
    raise TypeError(msg.format(start_indices, operand.shape))
  if not all(map(operator.ge, operand.shape, update.shape)):
    msg = ("dynamic_update_slice update shape must be smaller than operand "
           "shape, got update shape {} for operand shape {}.")
    raise TypeError(msg.format(update.shape, operand.shape))
  if any(idx.ndim != 0 for idx in start_indices):
    raise TypeError("start_indices arguments to dynamic_update_slice must be "
                    f"scalars, got indices {start_indices}")
  return operand.shape

