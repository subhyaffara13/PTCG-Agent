
def _scaled_matmul_batcher(batched_args, batch_dims, *, preferred_element_type):
  assert len(batch_dims) == 4
  assert (
      batch_dims[0] == batch_dims[1]
      and batch_dims[0] == batch_dims[2]
      and batch_dims[0] == batch_dims[3]
  )
  out_bdims = (batch_dims[0],)
  lhs, rhs, lhs_scales, rhs_scales = batched_args
  *batch, lhs_non_contracting, contracting = lhs.shape
  *_, _, scales_contracting = lhs_scales.shape
  *_, rhs_non_contracting, _ = rhs.shape

  new_batch = reduce(operator.mul, batch)
  # reshape to 3D shape
  lhs = jnp.reshape(lhs, (new_batch, lhs_non_contracting, contracting))
  lhs_scales = jnp.reshape(
      lhs_scales, (new_batch, lhs_non_contracting, scales_contracting)
  )
  rhs = jnp.reshape(rhs, (new_batch, rhs_non_contracting, contracting))
  rhs_scales = jnp.reshape(
      rhs_scales, (new_batch, rhs_non_contracting, scales_contracting)
  )
  output = jnp.reshape(
      _scaled_matmul_p_wrapper.bind(
          lhs,
          rhs,
          lhs_scales,
          rhs_scales,
          preferred_element_type=preferred_element_type,
      )[0],
      (*batch, lhs_non_contracting, rhs_non_contracting),
  )
  return (output,), out_bdims

