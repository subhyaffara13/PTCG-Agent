
def bind_psum_invariant(leaf, *, axes, axis_index_groups, is_async):
  if axis_index_groups is not None:
    raise NotImplementedError
  if (config.auto_pcast.value and
      (names := set(axes) - core.typeof(leaf).mat.varying)):
    leaf = pvary(leaf, tuple(names))
  prim = psum_invariant_start_p if is_async else psum_invariant_p
  return prim.bind(leaf, axes=axes)

