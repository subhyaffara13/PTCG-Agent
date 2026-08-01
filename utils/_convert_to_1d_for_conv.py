
def _convert_to_1d_for_conv(mat, index_dtype):
  if isinstance(mat, (jax.Array, np.ndarray)):
    data = lax.squeeze(mat, (0, 1))
    indices = lax.broadcasted_iota(index_dtype, (len(data), 1), 0)
  elif isinstance(mat, BCOO):
    mat = mat.update_layout(n_batch=2, n_dense=0)
    data = lax.squeeze(mat.data, (0, 1))
    indices = lax.squeeze(mat.indices, (0, 1))
    # zero-out data at OOB indices, otherwise strange things happen.
    data = jnp.where(lax.squeeze(indices, (1,)) < mat.shape[-1], data, 0)
  else:
    raise TypeError(f"bcoo_conv_general_dilated: input of type {type(mat)} not recognized.")
  return BCOO((data, indices), shape=mat.shape[2:])

