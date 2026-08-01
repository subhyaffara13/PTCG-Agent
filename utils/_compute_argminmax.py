
def _compute_argminmax(value_comparator, get_identity,
                       operand, *, index_dtype, axes):
  # value_comparator is either lax.lt (for argmin) or lax.gt
  # get_identity(operand.dtype) is inf for argmin or -inf for argmax
  axis, = axes
  indices = broadcasted_iota(
      index_dtype, np.shape(operand), axis,
      out_sharding=operand.aval.sharding)
  res = reduce([operand, indices],
               [get_identity(operand.dtype), np.array(0, index_dtype)],
               _ArgMinMaxReducer(value_comparator),
               axes)
  return res[1]

