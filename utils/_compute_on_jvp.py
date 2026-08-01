
def _compute_on_jvp(primals, tangents, *, jaxpr, compute_type,
                    out_memory_spaces, compiler_options_json):
  nzs = [not isinstance(t, ad.Zero) for t in tangents]
  jaxpr_jvp, out_nzs = ad.jvp_jaxpr(jaxpr, nzs, False)
  nz_tangents = [t for t in tangents if not isinstance(t, ad.Zero)]
  spaces_jvp = (*out_memory_spaces,
                *[s for s, nz in zip(out_memory_spaces, out_nzs) if nz])
  outs = compute_on_p.bind(*primals, *nz_tangents, jaxpr=jaxpr_jvp,
                           compute_type=compute_type,
                           out_memory_spaces=spaces_jvp,
                           compiler_options_json=compiler_options_json)
  primals_out, nz_tangents_out = outs[:len(out_nzs)], outs[len(out_nzs):]
  nz_outs = iter(nz_tangents_out)
  tangents_out = [next(nz_outs) if nz else ad.Zero(aval.to_tangent_aval())
                  for aval, nz in zip(jaxpr.out_avals, out_nzs)]
  assert next(nz_outs, None) is None
  return primals_out, tangents_out

