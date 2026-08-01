
def _cond_to_lojax(pred, *hi_args, branches, **kwds):
  jaxpr = branches[0]
  lo_branches = tuple(pe.lower_jaxpr2(j) for j in branches)
  lo_args = [lo_val for aval, x in zip(branches[0].in_aval_qdds, hi_args)
             for lo_val in (aval.read_loval(x) if aval.has_qdd
                            else aval.lower_val(x))]
  all_outs = cond_p.bind(pred, *lo_args, branches=lo_branches, **kwds)
  lo_muts_out = sum(len(aval.lo_ty()) for aval in branches[0].final_aval_qdds if aval.has_qdd)
  out_mut, lo_outs = split_list(all_outs, [lo_muts_out])

  # collect and apply mutations
  out_mut_ = iter(out_mut)
  in_idx = {v: i for i, v in enumerate(jaxpr.jaxpr.invars)}

  for v in jaxpr.jaxpr.invars:
    if v.final_qdd is not None:
      qdd = v.final_qdd
      lo_vals = itertools.islice(out_mut_, len(v.aval.lo_ty_qdd(qdd)))
      v.aval.update_from_loval(qdd, hi_args[in_idx[v]], *lo_vals)

  lo_outs_ = iter(lo_outs)

  hi_outs = [t.raise_val(*itertools.islice(lo_outs_, len(t.lo_ty())))
             for t in jaxpr.out_avals]
  assert next(lo_outs_, None) is None
  return hi_outs

