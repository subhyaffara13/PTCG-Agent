
def _bcoo_transpose_batch_rule(batched_args, batch_dims, *, permutation: Sequence[int], spinfo: SparseInfo):
  data, indices, spinfo = _bcoo_batch_dims_to_front(batched_args, batch_dims, spinfo)
  batched_permutation = (0, *(p + 1 for p in permutation))
  data, indices = _bcoo_transpose(data, indices, permutation=batched_permutation, spinfo=spinfo)
  batch_dims_out = [None if bdim is None else 0 for bdim in batch_dims]
  args_out = [lax.squeeze(arg, [0]) if bdim is None else arg
              for arg, bdim in zip((data, indices), batch_dims_out)]
  return args_out, batch_dims_out

