
def _get_reduce_scatter_dim(lhs, rhs, output):
  _, _, lhs_k_spec = lhs.spec
  _, _, rhs_k_spec = rhs.spec
  _, out_m_spec, out_n_spec = output.spec

  if lhs_k_spec == None or lhs_k_spec != rhs_k_spec:
    return None

  if out_m_spec == lhs_k_spec:
    return 1
  if out_n_spec == lhs_k_spec:
    return 2
  return None

