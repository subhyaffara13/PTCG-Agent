
def _broadcast_in_dim_shape_rule(operand, *, shape, broadcast_dimensions,
                                 sharding):
  _check_shapelike('broadcast_in_dim', 'shape', shape)
  _check_shapelike('broadcast_in_dim', 'broadcast_dimensions',
                   broadcast_dimensions)
  operand_ndim = np.ndim(operand)
  if operand_ndim != len(broadcast_dimensions):
    msg = ('broadcast_in_dim broadcast_dimensions must have length equal to '
           'operand ndim; got broadcast_dimensions {} for operand ndim {}.')
    raise TypeError(msg.format(broadcast_dimensions, operand_ndim))
  if len(shape) < operand_ndim:
    msg = ('broadcast_in_dim target broadcast shape must have equal or higher rank '
           'to the operand shape; got operand ndim {} and target broadcast ndim {}.')
    raise TypeError(msg.format(operand_ndim, len(shape)))
  if not set(broadcast_dimensions).issubset(set(range(len(shape)))):
    msg = ('broadcast_in_dim broadcast_dimensions must be a subset of output '
           'dimensions, got {} for operand ndim {} and shape {}.')
    raise TypeError(msg.format(broadcast_dimensions, operand_ndim, shape))
  if not all(core.definitely_equal_one_of_dim(operand.shape[i],
                                              [1, shape[broadcast_dimensions[i]]])
             for i in range(operand_ndim)):
    msg = (
        "broadcast_in_dim operand dimension sizes must either be 1, or be "
        "equal to their corresponding dimensions in the target broadcast "
        "shape; got operand of shape {}, target broadcast shape {}, "
        "broadcast_dimensions {} ")
    raise TypeError(msg.format(
        tuple(core.replace_tracer_for_error_message(d) for d in operand.shape),
        shape, broadcast_dimensions))
  if len(broadcast_dimensions) != len(set(broadcast_dimensions)):
    msg = ("broadcast_in_dim broadcast_dimensions must not contain duplicates, "
           "got broadcast_dimensions {}")
    raise TypeError(msg.format(broadcast_dimensions))
  return shape

