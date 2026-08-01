
def dynamic_slice_error_check(error, enabled_errors, operand, *start_indices, slice_sizes):
  out = lax.dynamic_slice_p.bind(operand, *start_indices, slice_sizes=slice_sizes)

  if OOBError not in enabled_errors:
    return error, out

  start_indices = jnp.array(start_indices)
  operand_dims = np.array(operand.shape, dtype=start_indices.dtype)
  slice_sizes = np.array(slice_sizes, dtype=start_indices.dtype)
  oob_mask = (start_indices < 0) | (start_indices + slice_sizes > operand_dims)

  payload = oob_payload(oob_mask, start_indices, range(operand.ndim), operand.shape)
  error = assert_func(error, jnp.any(oob_mask), OOBError(get_traceback(), "dynamic_slice", operand.shape, payload))
  return error, out

