
def _dot_batch_rule(
    unpack_args,
    unpack_dims,
    invoke_prim,
    axis_data,
    batched_args,
    batch_dims,
    *,
    dimension_numbers,
    out_sharding,
    precision,
    preferred_element_type: DTypeLike | None,
    **_,
):
  lhs, rhs = unpack_args(batched_args)
  lbd, rbd = unpack_dims(batch_dims)
  if lbd is None and rbd is None:
    out = invoke_prim(lhs, rhs, dimension_numbers, precision=precision,
                      preferred_element_type=preferred_element_type,
                      out_sharding=out_sharding)
    return out, None
  new_dimension_numbers, result_stack_dim = _dot_general_batch_dim_nums(
      (np.ndim(lhs), np.ndim(rhs)), (lbd, rbd),
      dimension_numbers)

  lhs_shape = np.shape(lhs)
  rhs_shape = np.shape(rhs)
  result_shape = _dot_general_shape_computation(lhs_shape, rhs_shape, new_dimension_numbers)
  result_batch_dim = canonicalize_axis(result_stack_dim, len(result_shape))

  if out_sharding is not None:
    out_sharding = batching.get_sharding_for_vmap(
        axis_data, out_sharding, result_batch_dim)

  batched_out = invoke_prim(
      lhs,
      rhs,
      new_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=out_sharding,
  )
  return batched_out, result_batch_dim

