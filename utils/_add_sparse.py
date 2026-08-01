
def _add_sparse(spenv, *spvalues):
  X, Y = spvalues
  out_shape = lax.broadcast_shapes(X.shape, Y.shape)
  if X.is_sparse() and Y.is_sparse():
    if X.shape != Y.shape:
      raise NotImplementedError("Addition between sparse matrices of different shapes.")
    if X.indices_ref == Y.indices_ref:
      out_data = lax.add(spenv.data(X), spenv.data(Y))
      if config.enable_checks.value:
        assert X.indices_sorted == Y.indices_sorted
        assert X.unique_indices == Y.unique_indices
      out_spvalue = spenv.sparse(X.shape, out_data, indices_ref=X.indices_ref,
                                 indices_sorted=X.indices_sorted,
                                 unique_indices=X.unique_indices)
    elif spenv.indices(X).ndim != spenv.indices(Y).ndim or spenv.data(X).ndim != spenv.data(Y).ndim:
      raise NotImplementedError("Addition between sparse matrices with different batch/dense dimensions.")
    else:
      out_indices = lax.concatenate([spenv.indices(X), spenv.indices(Y)], dimension=spenv.indices(X).ndim - 2)
      out_data = lax.concatenate([spenv.data(X), spenv.data(Y)], dimension=spenv.indices(X).ndim - 2)
      out_spvalue = spenv.sparse(X.shape, out_data, out_indices)
  else:
    if Y.is_sparse():
      X, Y = Y, X
    assert X.is_sparse() and Y.is_dense()
    if Y.shape != out_shape:
      raise NotImplementedError(
        "Addition between a sparse array X and a dense array Y is not implemented when "
        "the output shape is larger than Y.shape. This is to prevent silent densification "
        "of a large sparse array. If this is your intent, you can explicitly cast the sparse "
        "array to a dense matrix.")
    X_promoted, Y_promoted = spvalues_to_arrays(spenv, (X, Y))
    out = X_promoted.todense() + Y_promoted
    out_spvalue = spenv.dense(out)

  return (out_spvalue,)

