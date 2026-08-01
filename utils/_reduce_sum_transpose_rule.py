
def _reduce_sum_transpose_rule(cotangent, operand, *, axes, out_sharding):
  assert ad.is_undefined_primal(operand)
  input_shape = operand.aval.shape
  broadcast_dimensions = tuple(np.delete(np.arange(len(input_shape)), axes))
  result = broadcast_in_dim(
      cotangent, input_shape, broadcast_dimensions,
      out_sharding=operand.aval.sharding)
  assert result.shape == input_shape
  return [result]

