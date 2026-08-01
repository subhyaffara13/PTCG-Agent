
def _ref_lin(_is_vjp, nzs, x, *, memory_space, kind):
  nz, = nzs
  x_ref = core.ref_p.bind(x, memory_space=memory_space, kind=kind)
  def mut_lin(_, x_dot):
    if kind == 'no_grad_no_remat':
      aval = x_dot.aval if type(x_dot) is ad.Zero else core.typeof(x_dot)
      return ad.Zero(AbstractRef(aval))
    zero = ad_util.instantiate(x_dot)
    return core.ref_p.bind(zero, memory_space=memory_space, kind=kind)
  return x_ref, kind != 'no_grad_no_remat', None, mut_lin

