
def compare_jaxprs(jaxpr1, jaxpr2):
  """Compares two JAXPRs for symbolic equivalence."""
  sig1 = _jaxpr_signature(jaxpr1)
  sig2 = _jaxpr_signature(jaxpr2)
  return sig1 == sig2

