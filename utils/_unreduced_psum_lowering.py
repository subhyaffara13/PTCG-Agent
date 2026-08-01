
def _unreduced_psum_lowering(ctx, arg, *, axes):
  return _allreduce_lowering(lax.add_p, lax.reduce_sum, ctx, arg,
                             axes=axes, axis_index_groups=None)

