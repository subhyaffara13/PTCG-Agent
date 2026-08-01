
def _cond_jvp(primals, tangents, *, branches, **params):
  nonzeros = [type(t) is not ad_util.Zero for t in tangents]

  index_nz, *ops_nz = nonzeros
  assert index_nz is False

  branches_out_nz = [ad.jvp_jaxpr(jaxpr, ops_nz, instantiate=False)[1]
                     for jaxpr in branches]
  out_nz = [any(nz) for nz in zip(*branches_out_nz)]

  branches_jvp = tuple(ad.jvp_jaxpr(jaxpr, ops_nz, instantiate=out_nz)[0]
                       for jaxpr in branches)

  index, *ops = primals
  _, *ops_dot = tangents
  ops_dot = _prune_zeros(ops_dot)

  out = cond_p.bind(index, *ops, *ops_dot, branches=branches_jvp,
                    **params)
  out_primals, out_tangents = split_list(out, [len(out_nz)])
  out_tangents_iter = iter(out_tangents)
  out_tangents = [next(out_tangents_iter) if nz else
                  ad_util.p2tz(p)
                  for p, nz in zip(out_primals, out_nz)]
  return out_primals, out_tangents

