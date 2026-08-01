
def _pjit_key_type_signature(eqn):
  return jaxpr_type_signature(eqn.params['jaxpr'].jaxpr)

