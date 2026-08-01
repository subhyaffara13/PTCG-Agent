
def _free_ref_jvp(primals, tangents):
  [primal_ref], [tangent_ref] = primals, tangents
  core.free_ref(primal_ref)
  core.free_ref(tangent_ref)
  return (), ()

