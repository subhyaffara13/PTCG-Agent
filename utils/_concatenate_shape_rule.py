
def _concatenate_shape_rule(*operands, **kwargs):
  dimension = kwargs.pop('dimension')
  if not operands:
    msg = "concatenate expects at least one operand, got 0."
    raise TypeError(msg)
  if not all(isinstance(operand, ShapedArray) for operand in operands):
    msg = "All objects to concatenate must be arrays, got {}."
    op = next(op for op in operands if not isinstance(op, ShapedArray))
    raise TypeError(msg.format(type(op)))
  if len({operand.ndim for operand in operands}) != 1:
    msg = "Cannot concatenate arrays with different numbers of dimensions: got {}."
    raise TypeError(msg.format(", ".join(str(o.shape) for o in operands)))
  if not 0 <= dimension < operands[0].ndim:
    msg = "concatenate dimension out of bounds: dimension {} for shapes {}."
    raise TypeError(msg.format(dimension, ", ".join([str(o.shape) for o in operands])))
  shapes = [operand.shape[:dimension] + operand.shape[dimension+1:]
            for operand in operands]
  if shapes[:-1] != shapes[1:]:
    msg = ("Cannot concatenate arrays with shapes that differ in dimensions "
           "other than the one being concatenated: concatenating along "
           "dimension {} for shapes {}.")
    shapes = [operand.shape for operand in operands]
    raise TypeError(msg.format(dimension, ", ".join(map(str, shapes))))

  concat_size = sum(o.shape[dimension] for o in operands)
  ex_shape = operands[0].shape
  return ex_shape[:dimension] + (concat_size,) + ex_shape[dimension+1:]

