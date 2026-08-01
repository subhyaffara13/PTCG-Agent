
def _ragged_all_to_all_transpose(
    t, operand, output, input_offsets, send_sizes, output_offsets, recv_sizes,
    *, axis_name, axis_index_groups):
  if type(t) is ad.Zero:
    operand_t = ad.Zero(operand.aval) if ad.is_undefined_primal(operand) else None
    output_t = ad.Zero(output.aval) if ad.is_undefined_primal(output) else None
  else:
    zero = ad.zeros_like_aval(operand.aval)
    output_offsets_ = all_to_all(output_offsets, axis_name, 0, 0, tiled=True)
    input_offsets_ = all_to_all(input_offsets, axis_name, 0, 0, tiled=True)
    operand_t = ragged_all_to_all_p.bind(
        t, zero, output_offsets_, recv_sizes, input_offsets_, send_sizes,
        axis_name=axis_name, axis_index_groups=axis_index_groups)
    mask = control_flow.cumsum(
        lax.full(t.shape[0], 0, dtype='int32').at[output_offsets_].set(1)
        .at[output_offsets_ + recv_sizes].add(-1))
    mask = lax.expand_dims(mask, (*range(1, t.ndim),))
    mask = lax.broadcast_in_dim(mask, shape=t.shape, broadcast_dimensions=tuple(range(t.ndim)))
    output_t = lax.select(mask, lax._zeros(t), t)
  return [operand_t, output_t] + [None] * 4

