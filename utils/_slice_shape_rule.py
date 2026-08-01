
def _slice_shape_rule(operand, *, start_indices, limit_indices, strides):
  lax._check_shapelike("slice", "start_indices", start_indices)
  lax._check_shapelike("slice", "limit_indices", limit_indices)
  if operand.ndim != len(start_indices):
    msg = ("slice start_indices must have length equal to the number of "
           "dimensions of the operand, got indices {} for operand shape {}.")
    raise TypeError(msg.format(start_indices, operand.shape))
  if len(start_indices) != len(limit_indices):
    msg = ("slice limit_indices must have the same length as start_indices, "
           "got start_indices {} and limit_indices {}.")
    raise TypeError(msg.format(start_indices, limit_indices))
  if not all(map(operator.ge, operand.shape, limit_indices)):
    msg = ("slice limit_indices must be less than or equal to operand shape, "
           "got limit_indices {} for operand shape {}.")
    raise TypeError(msg.format(limit_indices, operand.shape))
  if not all(si >= 0 for si in start_indices):
    msg = ("slice start_indices must be greater than or equal to zero, "
           "got start_indices of {}.")
    raise TypeError(msg.format(start_indices))
  if not all(map(operator.ge, limit_indices, start_indices)):
    msg = ("slice limit_indices must be greater than or equal to start_indices,"
          " got start_indices {} and limit_indices {}.")
    raise TypeError(msg.format(start_indices, limit_indices))
  diff = tuple(map(operator.sub, limit_indices, start_indices))
  if strides is None or tuple(strides) == (1,) * len(operand.shape):
    return diff

  lax._check_shapelike("slice", "strides", strides)
  if len(strides) != operand.ndim:
    msg = ("slice strides must have length equal to the number of dimensions "
            "of the operand, got strides {} for operand shape {}.")
    raise TypeError(msg.format(strides, operand.shape))
  if not all(s >= 0 for s in strides):
    msg = "slice strides must be positive, got {}"
    raise TypeError(msg.format(strides))
  return tuple(core.stride_dim(d, window_size=1, window_stride=s)
               for d, s in zip(diff, strides))

