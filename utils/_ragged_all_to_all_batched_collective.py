
def _ragged_all_to_all_batched_collective(axis_data, vals_in, dims_in,
                                          axis_name, axis_index_groups):
  if all(bdim is None for bdim in dims_in) and axis_data.name not in axis_name:
    out = ragged_all_to_all_p.bind(*vals_in, axis_name=axis_name,
                                   axis_index_groups=axis_index_groups)
    return out, None
  if axis_data.name in axis_name:
    raise NotImplementedError("Please open a feature request!")
  if axis_index_groups:
    raise NotImplementedError("Please open a feature request!")
  size = axis_data.size

  def bdim_at_second(x, d):
    assert x.ndim == 2
    return (batching.broadcast(x, size, 1, None) if d is None else
            x if d == 1 else x.T)
  def merge(x): return x.reshape(-1, *x.shape[2:])
  def split(x): return x.reshape(size, -1, *x.shape[1:])

  operand, output = map(partial(batching.bdim_at_front, size=size), vals_in[:2], dims_in[:2])
  N, M = operand.shape[1], output.shape[1]
  input_offsets, send_sizes, output_offsets, recv_sizes = \
      map(bdim_at_second, vals_in[2:], dims_in[2:])
  input_offsets += lax.iota(input_offsets.dtype, size)[None, :] * N
  output_offsets += lax.iota(output_offsets.dtype, size)[None, :] * M
  vals_in = operand, output, input_offsets, send_sizes, output_offsets, recv_sizes
  result = split(ragged_all_to_all(*map(merge, vals_in), axis_name=axis_name))
  return result, 0

