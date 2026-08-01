
def _rev_shape_rule(operand, *, dimensions):
  _check_shapelike('rev', 'dimensions', dimensions)
  if len(set(dimensions)) != len(dimensions):
    msg = 'rev dimensions must be unique, got {}.'
    raise TypeError(msg.format(dimensions))
  if dimensions and not _max(dimensions) < operand.ndim:
    msg = ('rev dimensions must all be less than operand ndim, got dimensions '
           '{} for operand ndim {}.')
    raise TypeError(msg.format(dimensions, operand.ndim))
  return operand.shape

