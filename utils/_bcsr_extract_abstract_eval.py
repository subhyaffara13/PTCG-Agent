
def _bcsr_extract_abstract_eval(indices, indptr, mat):
  n_batch, n_dense, nse = _validate_bcsr_indices(indices, indptr, mat.shape)
  out_shape = mat.shape[:n_batch] + (nse,) + mat.shape[mat.ndim - n_dense:]
  return core.ShapedArray(out_shape, mat.dtype)

