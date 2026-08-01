
def _insert_reduce_precision(jaxpr: core.Jaxpr, num_res: int) -> core.Jaxpr:
  res_vars = jaxpr.outvars[len(jaxpr.outvars) - num_res:]
  used_vars = {x for e in jaxpr.eqns for x in e.invars if isinstance(x, core.Var)}
  invars, constvars, eqns = jaxpr.invars[:], jaxpr.constvars[:], jaxpr.eqns[:]
  for v in res_vars:
    if (not isinstance(v.aval, core.ShapedArray) or
        not dtypes.issubdtype(v.aval.dtype, np.inexact)):
      continue
    if v not in used_vars:
      continue
    assert isinstance(v, core.Var)
    newvar = core.Var(v.aval)
    finfo = dtypes.finfo(v.aval.dtype)
    params = dict(exponent_bits=finfo.nexp, mantissa_bits=finfo.nmant)
    if v in constvars or v in invars:
      lst = constvars if v in constvars else invars
      new_eqn = core.new_jaxpr_eqn(
          [newvar], [v], lax_internal.reduce_precision_p, params, set())
      lst[lst.index(v)] = newvar
      eqns.insert(0, new_eqn)
    else:
      (eqn_idx, eqn), = ((i, e) for i, e in enumerate(eqns) if v in e.outvars)
      if (eqn.primitive == lax_internal.reduce_precision_p and
          eqn.params == params):
        continue
      replace_eqn = eqn.replace(outvars=[v_ if v_ != v else newvar
                                         for v_ in eqn.outvars])
      new_eqn = core.new_jaxpr_eqn(
          [newvar], [v], lax_internal.reduce_precision_p, params, set(),
          eqn.source_info, eqn.ctx)
      eqns[eqn_idx] = replace_eqn
      eqns.insert(eqn_idx+1, new_eqn)
  new_jaxpr = jaxpr.replace(invars=invars, constvars=constvars, eqns=eqns)
  config.enable_checks.value and core.check_jaxpr(new_jaxpr)
  return new_jaxpr

