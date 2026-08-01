
def _mul_sparse(spenv, *spvalues, out_dtype=None):
  X, Y = spvalues
  if X.is_sparse() and Y.is_sparse():
    if X.indices_ref == Y.indices_ref and X.unique_indices:
      if config.enable_checks.value:
        assert X.indices_sorted == Y.indices_sorted
        assert X.unique_indices == Y.unique_indices
      out_data = lax.mul(spenv.data(X), spenv.data(Y), out_dtype=out_dtype)
      out_spvalue = spenv.sparse(X.shape, out_data, indices_ref=X.indices_ref,
                                 indices_sorted=X.indices_sorted,
                                 unique_indices=True)
    else:
      X_promoted, Y_promoted = spvalues_to_arrays(spenv, spvalues)
      if out_dtype is not None:
        X_promoted = X_promoted.astype(out_dtype)
        Y_promoted = Y_promoted.astype(out_dtype)
      mat = bcoo_multiply_sparse(X_promoted, Y_promoted)
      out_spvalue = spenv.sparse(mat.shape, mat.data, mat.indices)
  else:
    if Y.is_sparse():
      X, Y = Y, X
    X_promoted = spvalues_to_arrays(spenv, X)
    if out_dtype is not None:
      X_promoted = X_promoted.astype(out_dtype)
      Y = Y.astype(out_dtype)
    out_data = bcoo_multiply_dense(X_promoted, spenv.data(Y))
    out_spvalue = spenv.sparse(X.shape, out_data, indices_ref=X.indices_ref,
                               indices_sorted=X.indices_sorted,
                               unique_indices=X.unique_indices)

  return (out_spvalue,)

