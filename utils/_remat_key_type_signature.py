
def _remat_key_type_signature(eqn):
  # The assumption here is that the non-differentiated pass contains all relevant
  # key usage, and the differentiated pass
  #  1) will only consume keys that are already consumed in the non-differentiated pass
  #  2) will never create keys
  # Therefore, the differentiated pass is a no-op.
  if eqn.params['differentiated']:
    return KeyReuseSignature()
  return jaxpr_type_signature(eqn.params['jaxpr'])

