
def _reshape_shape_rule(operand, *, new_sizes, dimensions, sharding):
  if not all(d >= 0 for d in new_sizes):
    msg = 'reshape new_sizes must all be positive, got {}.'
    raise TypeError(msg.format(new_sizes))
  # TODO(necula): re-enable this check
  if dimensions is not None:
    if set(dimensions) != set(range(np.ndim(operand))):
      msg = ('reshape dimensions must be a permutation of operand dimensions, '
             'got dimensions {} for shape {}.')
      raise TypeError(msg.format(dimensions, np.shape(operand)))
  return tuple(new_sizes)

