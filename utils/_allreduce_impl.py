
def _allreduce_impl(prim, pos_reducer, arg, *, axes, axis_index_groups):
  assert axis_index_groups is None
  if not all(isinstance(axis, int) for axis in axes):
     return dispatch.apply_primitive(prim, arg, axes=axes,
                                     axis_index_groups=axis_index_groups)
  assert all(isinstance(axis, int) for axis in axes)
  return pos_reducer(arg, axes)

