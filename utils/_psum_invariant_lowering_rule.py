
def _psum_invariant_lowering_rule(ctx, arg, *, axes):
  return _allreduce_lowering(lax.add_p, lax.reduce_sum, ctx, arg, axes=axes,
                             axis_index_groups=None)

