
def _ragged_dot_general_batch_rule(
    axis_data,
    batched_args,
    batch_dims,
    *,
    ragged_dot_dimension_numbers,
    precision,
    preferred_element_type: DTypeLike | None,
    group_offset,
    out_sharding,
):
  invoke = partial(_ragged_dot_general_invoke_prim, batched_args[2])
  batched_out, result_batch_dim = _dot_batch_rule(
      _ragged_dot_batch_unpack_args,
      _ragged_dot_batch_unpack_dims,
      invoke,
      axis_data,
      batched_args,
      batch_dims,
      dimension_numbers=ragged_dot_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=None,
  )
  if _is_ragged_contracting(batched_args[0].ndim - 1,
                            ragged_dot_dimension_numbers):
    result_batch_dim += 1
  return batched_out, result_batch_dim

