
def _bcoo_sum_duplicates_batching_rule(batched_args, batch_dims, *, spinfo, nse):
  data, indices, new_spinfo = _bcoo_batch_dims_to_front(batched_args, batch_dims, spinfo)
  data_out, indices_out = bcoo_sum_duplicates_p.bind(data, indices, spinfo=new_spinfo, nse=nse)
  # Note: if data is unbatched on input, it will be batched on output.
  # However, if indices are unbatched on input, they will be unbatched on output.
  if batch_dims[1] is None:
    indices_out = lax.squeeze(indices_out, [0])
    out_axes = (0, None)
  else:
    out_axes = (0, 0)
  return (data_out, indices_out), out_axes

