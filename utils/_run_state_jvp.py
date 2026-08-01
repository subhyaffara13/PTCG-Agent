
def _run_state_jvp(primals: Sequence[Any], tangents: Sequence[Any], *,
                   jaxpr: core.Jaxpr, which_linear: tuple[bool, ...],
                   is_initialized: tuple[bool, ...]):
  if not all(is_initialized):
    raise NotImplementedError("Uninitialized Refs are not supported in jvp.")
  nonzero_tangents: list[bool] = [not isinstance(t, ad_util.Zero) for t in tangents]
  discharged_jaxpr = discharge_state(core.ClosedJaxpr(jaxpr, ()))
  for _ in range(len(nonzero_tangents)):
    _, out_nonzero_tangents = ad.jvp_jaxpr(
        discharged_jaxpr, nonzero_tangents, instantiate=nonzero_tangents)
    if out_nonzero_tangents == nonzero_tangents:
      break
    nonzero_tangents = map(operator.or_, nonzero_tangents, out_nonzero_tangents)
  else:
    raise Exception("Invalid fixpoint")
  del discharged_jaxpr, out_nonzero_tangents
  tangents = [ad.instantiate_zeros(t) if inst else t
              for t, inst in zip(tangents, nonzero_tangents)]
  tangents = [t for t in tangents if type(t) is not ad_util.Zero]
  closed_jvp_jaxpr, _ = ad.jvp_jaxpr(pe.close_jaxpr(jaxpr),
                                     nonzero_tangents, [])
  jvp_jaxpr_, jvp_consts = closed_jvp_jaxpr.jaxpr, closed_jvp_jaxpr.consts
  jvp_jaxpr = hoist_consts_to_refs(jvp_jaxpr_)
  jvp_which_linear = (*(False,) * len(jvp_consts), *which_linear, *(True,) * len(tangents))
  out = run_state_p.bind(*jvp_consts, *primals, *tangents, jaxpr=jvp_jaxpr,
                         which_linear=jvp_which_linear,
                         # TODO(sharadmv): compute this in the general case
                         is_initialized=(True,) * len(jvp_jaxpr.invars))
  out_consts, out_primals, out_tangents = split_list(out, [len(jvp_consts),
                                                           len(primals)])
  del out_consts
  out_tangents_iter = iter(out_tangents)
  out_tangents = [next(out_tangents_iter) if nz else ad_util.p2tz(p)
                  for p, nz in zip(out_primals, nonzero_tangents)]
  return out_primals, out_tangents

