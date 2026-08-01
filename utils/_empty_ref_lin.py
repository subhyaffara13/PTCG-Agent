
def _empty_ref_lin(_is_vjp, nzs_in, *, ty, memory_space):
  primal_ref = core.empty_ref_p.bind(ty=ty, memory_space=memory_space)
  def lin(_):
    return core.empty_ref_p.bind(ty=ty.to_tangent_aval(),
                                 memory_space=memory_space)
  return primal_ref, True, None, lin

