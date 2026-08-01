
def _jvp_jaxpr(jaxpr: core.ClosedJaxpr,
               nonzeros: Sequence[bool], instantiate: Sequence[bool]):
  assert len(jaxpr.in_avals) == len(nonzeros)
  primal_avals_in = ft.flatten_list(jaxpr.in_aval_qdds)
  tangent_avals_in = primal_avals_in.map(lambda aval: aval.to_tangent_aval())
  nz_tangent_avals_in = tangent_avals_in.map2(
      lambda aval, nz: aval if nz else Zero(aval), nonzeros).filter_with_mask(nonzeros)
  avals_in = ft.pack_args(primal_avals_in, nz_tangent_avals_in)
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  def f_jvp_traceable(primals, nonzero_tangents):
    tangents = nonzero_tangents.unfilter()
    primals_out, tangents_out = jvp(core.jaxpr_as_fun(jaxpr), primals, tangents,
                                    instantiate=instantiate,
                                    transform_stack=False)
    primals_out = ft.flatten_list(primals_out)
    tangents_out = ft.flatten_list(tangents_out).filter(lambda t: type(t) is not Zero)
    return ft.pack((primals_out, tangents_out))

  jaxpr, out_avals = pe.trace_to_jaxpr(f_jvp_traceable, avals_in, dbg,
                                       fun_takes_flat_tree_arg=True,
                                       fun_returns_flat_tree=True)

  _, nz_tangent_avals_out = out_avals.unpack()
  tangent_avals_out = nz_tangent_avals_out.unfilter()
  out_nonzeros = [type(t) is not Zero for t in tangent_avals_out]
  return jaxpr, out_nonzeros

