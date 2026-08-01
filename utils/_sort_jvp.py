
def _sort_jvp(primals, tangents, *, dimension, is_stable, num_keys):
  shape = primals[0].shape
  index_dtype = lax_utils.int_dtype_for_shape(shape, signed=False)
  sorted_primals_and_idx = sort_p.bind(
      *primals,
      broadcasted_iota(index_dtype, shape, dimension),
      dimension=dimension, is_stable=is_stable, num_keys=num_keys)
  batch_dims = tuple(np.delete(np.arange(len(shape), dtype=np.int64),
                               dimension))
  dnums = slicing.GatherDimensionNumbers(
    offset_dims=(),
    collapsed_slice_dims=(dimension,),
    start_index_map=(dimension,),
    operand_batching_dims=batch_dims,
    start_indices_batching_dims=batch_dims,
  )
  idx = expand_dims(sorted_primals_and_idx[-1], (len(shape),))
  gather_idx = partial(
    slicing.gather,
    start_indices=idx, dimension_numbers=dnums, slice_sizes=(1,) * len(shape),
    mode=slicing.GatherScatterMode.PROMISE_IN_BOUNDS
  )
  tangents_out = [t if type(t) is ad_util.Zero else gather_idx(t)
                  for t in tangents]
  return tuple(sorted_primals_and_idx[:-1]), tangents_out

