
def _dynamic_slice_dtype_rule(operand, *starts_and_dyn_sizes, slice_sizes):
  start_indices, dyn = util.split_list(starts_and_dyn_sizes, [operand.ndim])
  if any(i.dtype != start_indices[0].dtype or
         not dtypes.issubdtype(i.dtype, np.integer) for i in start_indices):
    msg = ("index arguments to dynamic_slice must be integers of the same "
           "type, got: {}")
    raise TypeError(msg.format(", ".join(i.dtype.name for i in start_indices)))
  return operand.dtype

