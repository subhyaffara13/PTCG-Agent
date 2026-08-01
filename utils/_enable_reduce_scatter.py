
def _enable_reduce_scatter(lhs, rhs):
  _, m_spec, lhs_k_spec = lhs.spec
  _, n_spec, rhs_k_spec = rhs.spec
  return (
      lhs_k_spec != None
      and lhs_k_spec == rhs_k_spec
      and m_spec != None
      and m_spec == n_spec
  )

