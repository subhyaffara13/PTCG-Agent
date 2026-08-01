
def _top_k_jvp(primals, tangents, *, k, axis):
  operand, = primals
  tangent, = tangents
  primals_out = top_k(operand, k, axis=axis)
  if type(tangent) is ad_util.Zero:
    tangent_out = ad_util.p2tz(primals_out[0])
  else:
    _, k_idxs = primals_out
    idx_shape = k_idxs.shape
    rank = len(idx_shape)
    gather_index_shape = idx_shape + (1,)
    gather_indices = reshape(k_idxs, gather_index_shape)
    slice_sizes = (1,) * rank
    dnums = slicing.GatherDimensionNumbers(
        offset_dims=(),
        collapsed_slice_dims=(axis,),
        operand_batching_dims=tuple(i for i in range(rank) if i != axis),
        start_indices_batching_dims=tuple(i for i in range(rank) if i != axis),
        start_index_map=(axis,))
    tangent_out = slicing.gather(tangent, gather_indices, dnums, slice_sizes)
  return primals_out, (tangent_out, ad_util.p2tz(primals_out[1]))

