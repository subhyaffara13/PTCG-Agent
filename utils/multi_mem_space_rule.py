
def multi_mem_space_rule(prim, num_out, *avals, **kwargs):
  out_mem_space = _default_memory_space_rule(prim, *avals, **kwargs)
  return [out_mem_space] * num_out

