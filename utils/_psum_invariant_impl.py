
def _psum_invariant_impl(arg, *, axes):
  return _allreduce_impl(psum_invariant_p, lax.reduce_sum, arg, axes=axes,
                         axis_index_groups=None)

