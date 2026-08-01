
def _standard_sparse_rule(prim, sparse_op):
  def _sparse_rule(spenv, *spvalues, **kwds):
    result = sparse_op(*spvalues_to_arrays(spenv, spvalues), **kwds)
    return arrays_to_spvalues(spenv, result if prim.multiple_results else [result])
  return _sparse_rule

