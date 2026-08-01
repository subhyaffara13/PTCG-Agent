
def dce(traced):
  jaxpr_, used = pe.dce_jaxpr(traced.jaxpr.jaxpr, True)
  jaxpr = core.ClosedJaxpr(jaxpr_, traced.jaxpr.consts)
  used_res, used_primals = split_list(used, [traced._num_consts])
  res = [r for r, u in zip(traced._consts, used_res) if u]
  return used_primals, Partial(partial(_dced, jaxpr, traced.out_tree), res)

