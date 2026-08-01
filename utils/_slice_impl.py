
def _slice_impl(x, start_indices, limit_indices, strides):
  if strides is not None:
    return dispatch.apply_primitive(
      slice_p, x, start_indices=start_indices,
      limit_indices=limit_indices, strides=strides)
  slice_sizes = tuple(np.array(limit_indices) - np.array(start_indices))
  return dispatch.apply_primitive(dynamic_slice_p, x, *start_indices,
                                  slice_sizes=slice_sizes)

