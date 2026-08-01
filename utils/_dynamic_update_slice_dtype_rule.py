
def _dynamic_update_slice_dtype_rule(operand, update, *start_indices):
  lax.check_same_dtypes("dynamic_update_slice", operand, update)
  if any(i.dtype != start_indices[0].dtype or
         not dtypes.issubdtype(i.dtype, np.integer) for i in start_indices):
    msg = ("index arguments to dynamic_update_slice must be integers of the "
           "same type, got {}")
    raise TypeError(msg.format(", ".join(i.dtype.name for i in start_indices)))
  return operand.dtype

