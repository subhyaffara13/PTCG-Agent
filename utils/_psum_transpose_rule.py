
def _psum_transpose_rule(cts, arg, *, axes, axis_index_groups):
  named_axes, pos_axes = axes_partition = [], []
  for axis in axes:
    axes_partition[isinstance(axis, int)].append(axis)

  if pos_axes:
    def broadcast_positional(ct, arg):
      assert ad.is_undefined_primal(arg)
      if type(ct) is ad.Zero: return ad.Zero(arg.aval)
      return lax._reduce_sum_transpose_rule(ct, arg, axes=pos_axes,
                                            out_sharding=None)[0]
    cts = broadcast_positional(cts, arg)

  # We treat psum as psum + pbroadcast, which is why the transpose reduces
  # over the named axes again (unlike for positional axes).
  return (psum_p.bind(cts, axes=tuple(named_axes),
                      axis_index_groups=axis_index_groups),)

