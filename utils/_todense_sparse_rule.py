
def _todense_sparse_rule(spenv, spvalue, *, tree):
  del tree  # TODO(jakvdp): we should assert that tree is PytreeDef(*)
  out = spvalues_to_arrays(spenv, spvalue).todense()
  return (spenv.dense(out),)

