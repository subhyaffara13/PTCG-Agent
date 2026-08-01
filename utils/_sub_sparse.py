
def _sub_sparse(spenv, *spvalues):
  X, Y = spvalues
  if X.is_sparse() and Y.is_sparse():
    return _add_sparse(spenv, X, *sparse_rules_bcoo[lax.neg_p](spenv, Y))
  else:
    raise NotImplementedError("Subtraction between sparse and dense array.")

