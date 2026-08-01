
def _div_sparse(spenv, *spvalues):
  X, Y = spvalues
  if Y.is_sparse():
    raise NotImplementedError(
      "Division by a sparse array is not implemented because it "
      "would result in dense output. If this is your intent, use "
      "sparse.todense() to convert your arguments to a dense array.")
  X_promoted = spvalues_to_arrays(spenv, X)
  out_data = bcoo_multiply_dense(X_promoted, 1. / spenv.data(Y))
  out_spvalue = spenv.sparse(X.shape, out_data, indices_ref=X.indices_ref,
                              indices_sorted=X.indices_sorted,
                              unique_indices=X.unique_indices)
  return (out_spvalue,)

