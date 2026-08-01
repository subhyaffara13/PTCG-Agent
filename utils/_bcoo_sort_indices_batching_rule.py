
def _bcoo_sort_indices_batching_rule(batched_args, batch_dims, *, spinfo):
  data, indices, spinfo = _bcoo_batch_dims_to_front(batched_args, batch_dims, spinfo)
  data_out, indices_out = bcoo_sort_indices_p.bind(data, indices, spinfo=spinfo)
  out_axes = (0, 0)
  # Note: if data is unbatched on input, it will be batched on output.
  # However, if indices are unbatched on input, they will be unbatched on output.
  if batch_dims[1] is None:
    indices_out = indices_out[0]
    out_axes = (0, None)
  return (data_out, indices_out), out_axes

