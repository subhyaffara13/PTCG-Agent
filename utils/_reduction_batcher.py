
def _reduction_batcher(prim, v, d, *, axes, axis_index_groups):
  assert not prim.multiple_results
  if not any(isinstance(axis, int) for axis in axes):
    out = (prim.bind(v, axes=axes) if prim is psum_invariant_p else
           prim.bind(v, axes=axes, axis_index_groups=axis_index_groups))
    return out, d
  val_out = _reduction_with_positional_batcher(
      prim, v, d, axis_index_groups,
      lambda d, v: (axes, v),
      lambda d, v: (tuple(axis + (axis >= d) if isinstance(axis, int) else axis
                          for axis in axes),
                    v))
  # _reduction_with_positional_batcher moves all map dims to 0
  return val_out, d if d is None else 0

