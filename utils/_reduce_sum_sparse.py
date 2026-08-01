
def _reduce_sum_sparse(spenv, *spvalues, axes, out_sharding):
  X, = spvalues
  X_promoted = spvalues_to_arrays(spenv, X)
  mat = sparse.bcoo_reduce_sum(X_promoted, axes=axes)
  out_shape = mat.shape
  if out_shape == ():
    out_spvalue = spenv.dense(mat.data.sum())
  else:
    out_spvalue = spenv.sparse(out_shape, mat.data, mat.indices)
  return (out_spvalue,)

