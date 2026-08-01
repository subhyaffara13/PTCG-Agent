
def _scaled_dot_batching_rule(
    batched_args, batch_dims, *, dimension_numbers, preferred_element_type
):
  # Unpack arguments and batch dimensions for inputs.
  lhs, rhs, lhs_scale, rhs_scale = batched_args
  lhs_bdim, rhs_bdim, lhs_scale_bdim, rhs_scale_bdim = batch_dims

  # Determine the batch size from the first argument that has a batch dimension.
  # We iterate through args and corresponding batch dims; if bdim is not None,
  # it means that argument is batched, so we take its size at that dimension.
  size = next(
      x.shape[d] for x, d in zip(batched_args, batch_dims) if d is not None
  )

  # Ensure the batch dimension is at the front (index 0) for all inputs.
  # If an input is broadcasted (bdim is None), this broadcasts it to include
  # the batch dimension at the front. If it is already batched but at a
  # different index, it moves it to 0.
  lhs = batching.bdim_at_front(lhs, lhs_bdim, size)
  rhs = batching.bdim_at_front(rhs, rhs_bdim, size)
  if lhs_scale is not None:
    lhs_scale = batching.bdim_at_front(lhs_scale, lhs_scale_bdim, size)
  if rhs_scale is not None:
    rhs_scale = batching.bdim_at_front(rhs_scale, rhs_scale_bdim, size)

  # Unpack the original dimension numbers.
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers

  # Since we moved the batch dimension to index 0 for all inputs, all existing
  # dimension indices must be shifted by 1.
  lhs_contract = tuple(d + 1 for d in lhs_contract)
  rhs_contract = tuple(d + 1 for d in rhs_contract)
  lhs_batch = tuple(d + 1 for d in lhs_batch)
  rhs_batch = tuple(d + 1 for d in rhs_batch)

  # Add the new leading batch dimension (index 0) to the set of batch dimensions
  # for both LHS and RHS. This effectively batches the operation.
  new_lhs_batch = (0,) + lhs_batch
  new_rhs_batch = (0,) + rhs_batch

  # Reconstruct dimension_numbers with the shifted and new indices.
  new_dimension_numbers = (
      (lhs_contract, rhs_contract),
      (new_lhs_batch, new_rhs_batch),
  )

  # Bind the primitive with the batched operands and updated dimension numbers.
  # This creates the batched scaled_dot operation in the jaxpr.
  result = scaled_dot_p.bind(
      lhs,
      rhs,
      lhs_scale,
      rhs_scale,
      dimension_numbers=new_dimension_numbers,
      preferred_element_type=preferred_element_type,
  )

  # Return the result and the index of the batch dimension in the result (0).
  return result, 0

