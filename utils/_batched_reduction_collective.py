
def _batched_reduction_collective(prim, if_unmapped, axis_data, vals_in,
                                  dims_in, axes, axis_index_groups):
  assert not prim.multiple_results
  (v,), (d,) = vals_in, dims_in
  del vals_in, dims_in

  if d is None:
    if axis_data.name in axes:
      return _constant_reduction(prim, axis_data, v, axes, axis_index_groups)
    else:
      out = (prim.bind(v, axes=axes) if prim is psum_invariant_p else
             prim.bind(v, axes=axes, axis_index_groups=axis_index_groups))
      return out, d

  if axis_data.name not in axes:
    return _reduction_batcher(
        prim, v, d, axes=axes, axis_index_groups=axis_index_groups)

  # Note that we have a choice here. We can either unfuse the reduction into one
  # that handles the batched dims and then another one that handles the rest.
  # Alternatively, we can keep the dimension reduction fused with the rest, but
  # we have to split the primitive into one for unmapped inputs and another
  # one for mapped, because they differ in their `axes` parameter.
  # We choose the second strategy here.
  val_out = _reduction_with_positional_batcher(
      prim, v, d, axis_index_groups,
      lambda d, v: (tuple(axis for axis in axes if axis != axis_data.name),
                    if_unmapped(v, axis_data.size)),
      lambda d, v: (tuple(axis + (axis >= d) if isinstance(axis, int) else axis
                          if axis != axis_data.name else d for axis in axes),
                    v))
  return val_out, None

