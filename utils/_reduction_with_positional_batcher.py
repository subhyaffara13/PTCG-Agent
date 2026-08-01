
def _reduction_with_positional_batcher(
    prim, v, d, axis_index_groups, transform_unmapped, transform_mapped):
  if axis_index_groups is not None:
    raise NotImplementedError("axis_index_groups not supported in vmap collectives. "
                              "Please open a feature request!")
  v = v if d is None or d == 0 else _moveaxis(d, 0, v)
  if d is None:
    unmapped_axes, unmapped_vals_in = transform_unmapped(0, v)
    return (prim.bind(unmapped_vals_in, axes=unmapped_axes)
            if prim is psum_invariant_p else
            prim.bind(unmapped_vals_in, axes=unmapped_axes, axis_index_groups=None))

  mapped_axes, mapped_vals_in = transform_mapped(0, v)
  return (prim.bind(mapped_vals_in, axes=mapped_axes)
          if prim is psum_invariant_p else
          prim.bind(mapped_vals_in, axes=mapped_axes, axis_index_groups=None))

