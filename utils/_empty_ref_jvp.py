
def _empty_ref_jvp(primals, tangents, *, ty, memory_space):
  primal_ref = core.empty_ref_p.bind(ty=ty, memory_space=memory_space)
  tangent_ref = core.empty_ref_p.bind(ty=ty.to_tangent_aval(),
                                      memory_space=memory_space)
  return primal_ref, tangent_ref

