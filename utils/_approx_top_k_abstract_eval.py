
def _approx_top_k_abstract_eval(operand, *, k, reduction_dimension,
                                recall_target, is_max_k,
                                reduction_input_size_override,
                                aggregate_to_topk):
  if k <= 0:
    raise ValueError(f'k must be positive, got {k}')
  if len(operand.shape) == 0:
    raise TypeError('approx_top_k operand must have >= 1 dimension, got {}'.format(
        operand.shape))
  dims = list(operand.shape)
  if dims[reduction_dimension] < k:
    raise ValueError(
        'k must be smaller than the size of reduction_dim {}, got {}'.format(
            dims[reduction_dimension], k))
  if not dtypes.issubdtype(operand.dtype, np.floating):
    raise ValueError('operand must be a floating type')
  reduction_input_size = dims[reduction_dimension]
  if aggregate_to_topk:
    dims[reduction_dimension] = k
  elif core.is_constant_shape((reduction_input_size, k)):
    dims[reduction_dimension] = _jax.approx_top_k_reduction_output_size(
        reduction_input_size, len(dims), k, recall_target, aggregate_to_topk,
        reduction_input_size_override)[0]
  else:
    raise NotImplementedError(
         "approx_top_k with aggregate_to_topk=False not yet implemented when "
         f"either the `k` ({k}) or the "
         f" reduction dimension size ({reduction_input_size}) are symbolic")
  operand_s = operand.sharding
  if operand_s.spec[reduction_dimension] is not None:
    raise core.ShardingTypeError(
        f"reduction dimension {reduction_dimension} in operand"
        f" {operand.str_short()} should be unsharded i.e. the spec of that dim"
        " should be `None`.")
  return (operand.update(shape=dims, dtype=operand.dtype,
                         weak_type=operand.weak_type,
                         manual_axis_type=operand.mat, sharding=operand_s),
          operand.update(shape=dims, dtype=np.dtype(np.int32),
                         manual_axis_type=operand.mat, sharding=operand_s))

