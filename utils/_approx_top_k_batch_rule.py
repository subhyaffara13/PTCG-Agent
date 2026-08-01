
def _approx_top_k_batch_rule(batch_operands, batch_axes, *, k,
                             reduction_dimension, recall_target, is_max_k,
                             reduction_input_size_override, aggregate_to_topk):
  assert len(batch_operands) == 1
  assert len(batch_axes) == 1
  operand, = batch_operands
  batch_axis, = batch_axes
  dim_map = [d for d in range(operand.ndim) if d is not batch_axis]
  reduction_dimension = dim_map[reduction_dimension]
  return approx_top_k_p.bind(
      operand,
      k=k,
      reduction_dimension=reduction_dimension,
      recall_target=recall_target,
      is_max_k=is_max_k,
      reduction_input_size_override=reduction_input_size_override,
      aggregate_to_topk=aggregate_to_topk), (batch_axis, batch_axis)

