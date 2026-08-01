
def _enable_all_reduce(lhs, rhs):
  _, _, lhs_k_spec = lhs.spec
  _, n_spec, rhs_k_spec = rhs.spec
  return lhs_k_spec != None and lhs_k_spec == rhs_k_spec and n_spec == None

