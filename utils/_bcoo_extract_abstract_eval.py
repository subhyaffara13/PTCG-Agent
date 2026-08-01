
def _bcoo_extract_abstract_eval(indices, arr, *, assume_unique):
  _ = bool(assume_unique)
  n_batch, _, n_dense, nse = _validate_bcoo_indices(indices, arr.shape)
  out_shape = arr.shape[:n_batch] + (nse,) + arr.shape[arr.ndim - n_dense:]
  return core.ShapedArray(out_shape, arr.dtype)

