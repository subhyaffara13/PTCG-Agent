
def dynamic_update_slice_error_check(error, enabled_errors, operand, update, *start_indices):
  out = lax.dynamic_update_slice_p.bind(operand, update, *start_indices)

  if OOBError not in enabled_errors:
    return error, out

  operand_dims = np.array(operand.shape)
  update_dims = np.array(update.shape)
  start_indices = jnp.array(start_indices)
  oob_mask = (start_indices < 0) | (start_indices + update_dims > operand_dims)

  payload = oob_payload(oob_mask, start_indices, range(operand.ndim), operand.shape)
  error = assert_func(error, jnp.any(oob_mask), OOBError(get_traceback(), "dynamic_update_slice", operand.shape, payload))
  return error, out

