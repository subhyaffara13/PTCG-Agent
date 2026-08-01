
def _all_gather_invariant_transpose_rule(
    cts, x, *, all_gather_dimension, axis_name, axis_size, tiled):
  slice_size, rem = divmod(cts.shape[all_gather_dimension], axis_size)
  assert not rem
  idx = axis_index(axis_name) * slice_size
  out = slicing.dynamic_slice_in_dim(
      cts, idx, slice_size=slice_size, axis=all_gather_dimension)
  return (out,) if tiled else (lax.squeeze(out, [all_gather_dimension]),)

