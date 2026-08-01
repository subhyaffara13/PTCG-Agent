
def scatter_oob(operand, indices, updates, dnums):
  # Ref: see clamping code used in scatter_translation_rule
  slice_sizes = []
  pos = 0
  for i in range(len(operand.shape)):
    if i in dnums.inserted_window_dims:
      slice_sizes.append(1)
    else:
      slice_sizes.append(updates.shape[dnums.update_window_dims[pos]])
      pos += 1

  upper_bound = np.array([operand.shape[i] - slice_sizes[i]
                          for i in dnums.scatter_dims_to_operand_dims],
                         np.int64)
  upper_bound = np.minimum(upper_bound, np.iinfo(indices.dtype).max)
  upper_bound = lax.broadcast_in_dim(upper_bound, indices.shape,
                                     (len(indices.shape) - 1,))

  lower_oob = jnp.less(indices, 0)
  upper_oob = jnp.greater(indices, upper_bound.astype(indices.dtype))
  oob_mask = jnp.logical_or(lower_oob, upper_oob)
  payload = oob_payload(oob_mask, indices,
                        dnums.scatter_dims_to_operand_dims, operand.shape)
  return jnp.any(oob_mask), payload

