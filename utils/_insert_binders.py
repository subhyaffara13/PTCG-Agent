
def _insert_binders(jaxpr, n_after, vals):
  avals = _map(typeof, vals)
  invars = [core.Var(lo_ty) for a, x in zip(avals, vals) for lo_ty in
            (a.lo_ty_qdd(cur_qdd(x)) if a.has_qdd else a.lo_ty())]
  invars = jaxpr.jaxpr.invars[:n_after] + invars + jaxpr.jaxpr.invars[n_after:]
  return jaxpr.replace(jaxpr=jaxpr.jaxpr.replace(invars=invars))

