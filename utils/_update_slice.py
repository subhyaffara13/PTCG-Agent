
def _update_slice(operand, update, start_indices, update_dims):
  """
  Similar to lax.dynamic_update_slice, but handles padded updates where padding
  values should not overwrite existing values in the array.

  Args:
  operand: the array to update
  update: the padded array to write
  start_indices: the offset at which to write `update`.
  update_dims: the true dimensions of the padded update `update`. Only values
    inside the rectangle given by `update_dims` will be overwritten."""
  operand_shape = operand.shape
  operand = lax.pad(operand,
                    jnp.array(0, operand.dtype),
                    [(0, d, 0) for d in update.shape])
  start_indices = tuple(jnp.array(i, np.int32) for i in start_indices)
  t = lax.dynamic_slice(operand, start_indices, update.shape)
  t = _mask(update, update_dims, t)
  operand = lax.dynamic_update_slice(operand, t, start_indices)
  return lax.slice(operand, [0] * operand.ndim, operand_shape)

