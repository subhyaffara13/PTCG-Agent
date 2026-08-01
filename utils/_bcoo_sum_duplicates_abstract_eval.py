
def _bcoo_sum_duplicates_abstract_eval(data, indices, *, spinfo, nse):
  if nse is None:
    raise ValueError("bcoo_sum_duplicates: nse must be specified when using the function within "
                     "jit, vmap, and other transformations requiring abstract evaluation.")
  props = _validate_bcoo(data, indices, spinfo.shape)
  indices_out = core.ShapedArray((*indices.shape[:props.n_batch], nse, props.n_sparse),
                                  dtype=indices.dtype, weak_type=indices.weak_type)
  data_out = core.ShapedArray(
    (*map(max, indices.shape[:props.n_batch], data.shape[:props.n_batch]),
     nse, *data.shape[props.n_batch + 1:]), data.dtype, weak_type=data.weak_type)
  return data_out, indices_out

