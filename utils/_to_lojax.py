
def _to_lojax(*hi_args, jaxpr, **params):
  # convert closed-over boxes to explicit args
  jaxpr, closed_over_himutables = pe.convert_const_himutables(jaxpr)
  hi_args = [*closed_over_himutables, *hi_args]
  params = _converted_mutables_add_params(len(closed_over_himutables), **params)

  lo_args_lol = [aval.read_loval_in(x) if aval.has_qdd else aval.lower_val(x)
                 for aval, x in zip(jaxpr.in_aval_qdds, hi_args)]
  lo_args = [x for xs in lo_args_lol for x in xs]

  in_avals = FlatTree.flatten(([[typeof(x) for x in xs] for xs in lo_args_lol], {}))
  lo_jaxpr, out_avals = pe.lower_jaxpr(jaxpr, in_avals)
  params = _lojax_expand_params(in_avals, out_avals, **params)

  all_outs = jit_p.bind(*lo_args, jaxpr=lo_jaxpr, **params)
  out_mut, lo_outs = out_avals.update(all_outs).unpack()
  for a, x, u in zip(jaxpr.final_aval_qdds, hi_args, out_mut.unpack()):
    if a.has_qdd:
      a.aval.update_from_loval2(a.qdd, x, u)
  return [a.raise_val2(y) for a, y in zip(jaxpr.out_avals, lo_outs.unpack())]

