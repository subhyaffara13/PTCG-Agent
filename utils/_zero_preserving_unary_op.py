
def _zero_preserving_unary_op(prim, linear):
  def func(spenv, *spvalues, **kwargs):
    assert len(spvalues) == 1
    spvalue = spvalues[0]
    if not linear:
      # For non-linear unary operations, we need to ensure that
      # indices are unique before applying the operator elementwise.
      spvalue = _ensure_unique_indices(spenv, spvalue)
    buf = spenv.data(spvalue)
    buf_out = prim.bind(buf, **kwargs)
    if spvalues[0].is_sparse():
      out_spvalue = spenv.sparse(spvalue.shape, buf_out,
                                 indices_ref=spvalue.indices_ref,
                                 indptr_ref=spvalue.indptr_ref,
                                 indices_sorted=spvalue.indices_sorted,
                                 unique_indices=spvalue.unique_indices)
    else:
      out_spvalue = spenv.dense(buf)
    return (out_spvalue,)
  return func

