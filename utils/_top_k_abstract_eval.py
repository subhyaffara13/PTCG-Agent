
def _top_k_abstract_eval(operand, *, k, axis):
  if dtypes.issubdtype(operand.dtype, np.complexfloating):
    raise ValueError("top_k is not compatible with complex inputs.")
  if k < 0:
    raise ValueError(f"k argument to top_k must be nonnegative, got {k}")
  if len(operand.shape) == 0:
    raise TypeError("top_k operand must have >= 1 dimension, got {}"
                    .format(operand.shape))
  if not (0 <= axis < len(operand.shape)):
    raise ValueError(f"axis argument out of range: {axis=} for {operand.shape=}")
  shape = list(operand.shape)
  if shape[axis] < k:
    raise ValueError("k argument to top_k must be no larger than size along axis;"
                     f" got {k=} with {shape=} and {axis=}")
  int32_max = dtypes.iinfo('int32').max
  try:
    too_large = (shape[axis] > int32_max + 1)
  except core.InconclusiveDimensionOperation:
    pass
  else:
    if too_large:
      raise ValueError(
          'top_k returns int32 indices, which will overflow for array'
          f' dimensions larger than the maximum int32 ({int32_max}). Got'
          f' {operand.shape=}')
  shape[axis] = k
  if operand.sharding.spec[axis] is not None:
    raise core.ShardingTypeError(
        'The input should be unsharded over the axis along which to compute the'
        f' top_k values. Got input type={operand} and axis={axis}')
  return (operand.update(shape=shape),
          operand.update(shape=shape, dtype=np.dtype(np.int32)))

