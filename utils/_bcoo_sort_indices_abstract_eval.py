
def _bcoo_sort_indices_abstract_eval(data, indices, *, spinfo):
  props = _validate_bcoo(data, indices, spinfo.shape)
  if props.n_sparse == 0:
    return data, indices
  data_out = core.ShapedArray(
    (*map(max, indices.shape[:props.n_batch], data.shape[:props.n_batch]),
     props.nse, *data.shape[props.n_batch + 1:]), data.dtype, weak_type=data.weak_type)
  return data_out, indices

