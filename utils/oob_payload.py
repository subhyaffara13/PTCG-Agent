
def oob_payload(oob_mask, indices, dims_map, operand_shape):
  # Get first OOB index, axis and axis size so it can be added to the error msg.
  flat_idx = jnp.argmin(jnp.logical_not(oob_mask))
  multi_idx = jnp.unravel_index(flat_idx, indices.shape)
  oob_axis = jnp.array(dims_map)[multi_idx[-1]]
  oob_axis_size = jnp.array(operand_shape)[oob_axis]
  oob_index = jnp.ravel(indices)[flat_idx]
  payload = jnp.array([oob_index, oob_axis, oob_axis_size], dtype=np.int32)
  return payload

