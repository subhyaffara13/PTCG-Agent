
def _fusible_to_lojax(*hi_args, jaxpr, num_consts, **_):
  const_in_avals = jaxpr.in_aval_qdds[:num_consts]
  num_lo_consts = sum(len(aval.lo_ty()) for aval in const_in_avals)

  lo_args = [
      lo_val
      for aval, x in util.safe_zip(jaxpr.in_aval_qdds, hi_args)
      for lo_val in (aval.read_loval(x) if aval.has_qdd else aval.lower_val(x))
  ]

  closed_jaxpr = jax_core.ClosedJaxpr(jaxpr, lo_args[:num_lo_consts])

  lo_jaxpr = pe.lower_jaxpr2(closed_jaxpr)
  all_outs = fusible_p.bind(*lo_args, jaxpr=lo_jaxpr.jaxpr, num_consts=num_lo_consts)

  out_mut, lo_outs = util.split_list(all_outs, [pe.num_himuts_out(jaxpr.final_aval_qdds)])
  for a, x, us in zip(jaxpr.final_aval_qdds, hi_args, out_mut):
    if a.has_qdd:
      a.aval.update_from_loval(a.qdd, x, *us)
  return pe.raise_lo_outs(jaxpr.out_avals, lo_outs)

