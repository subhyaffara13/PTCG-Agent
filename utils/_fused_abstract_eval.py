
def _fused_abstract_eval(*in_avals, out_spaces, jaxpr):
  return [a.update(memory_space=s)
          for a, s in zip(jaxpr.out_avals, out_spaces)]

