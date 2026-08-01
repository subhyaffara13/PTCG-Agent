
def _dynamic_slice_shape_rule(operand, *start_indices, slice_sizes):
  if not all(map(operator.ge, operand.shape, slice_sizes)):
    msg = ("slice slice_sizes must be less than or equal to operand shape, "
           "got slice_sizes {} for operand shape {}.")
    raise TypeError(msg.format(slice_sizes, operand.shape))
  if not all(ssz >= 0 for ssz in slice_sizes):
    msg = ("slice slice_sizes must be greater than or equal to zero, "
           "got slice_sizes of {}.")
    raise TypeError(msg.format(slice_sizes))
  if any(idx.ndim != 0 for idx in start_indices):
    raise TypeError("start_indices arguments to dynamic_slice must be scalars, "
                    f" got indices {start_indices}")
  return tuple(slice_sizes)

