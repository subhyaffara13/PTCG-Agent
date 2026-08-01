
def _shard_map_jvp(trace, shard_map_p, f, tracers, mesh, in_specs,
                   check_vma, newly_manual_axes, debug_info):
  debug_info = debug_info.with_unknown_names()
  primals, tangents = unzip2(map(trace.to_primal_tangent_pair, tracers))
  which_nz = [     type(t) is not ad.Zero           for t in tangents]
  tangents = [t if type(t) is not ad.Zero else None for t in tangents]
  args, in_zeros_tree = tree_flatten((primals, tangents))
  tangent_in_specs = [sp.to_tangent_spec() for sp, nz in zip(in_specs, which_nz) if nz]

  def f_jvp(*primals_and_nz_tangents_flat):
    primals, tangents = tree_unflatten(in_zeros_tree, primals_and_nz_tangents_flat)
    tangents = [ad.p2tz(p) if t is None else t for p, t in zip(primals, tangents)]
    primals_out_aux, tangents_out = ad.jvp_subtrace_2(f, trace.tag, primals, tangents)
    primals_out_ft, out_ax = primals_out_aux.unpack_aux()
    which_nz_out = [type(r) is not ad.Zero for r in tangents_out]
    tangent_out_specs = [s.to_tangent_spec() for s, nz in zip(out_ax, which_nz_out) if nz]
    new_out_specs = (*out_ax, *tangent_out_specs)
    tangents_out = [None if not nz else t for t, nz in zip(tangents_out, which_nz_out)]
    tangents_out_ft = FlatTree.flatten(list(tangents_out))
    out_primals_tangents = FlatTree.pack((primals_out_ft, tangents_out_ft))
    return out_primals_tangents.with_aux(which_nz_out).with_aux(new_out_specs)

  params = dict(mesh=mesh, in_specs=(*in_specs, *tangent_in_specs),
                check_vma=check_vma, newly_manual_axes=newly_manual_axes,
                debug_info=debug_info.with_unknown_names())
  avals = [typeof(x) for x in args]
  result = shard_map_p.bind_with_trace(
      trace.parent_trace, tuple(args), avals, dict(params, subfuns=(f_jvp,)))
  pt_out, which_nz_out = result.unpack_aux()
  primal_out, nz_tangents_out = pt_out.unpack()
  tangents_stack = list(nz_tangents_out)[::-1]
  make_tracer = lambda p, nz: ad.JVPTracer(trace, p, tangents_stack.pop()) if nz else p
  tracers_out = primal_out.map2(make_tracer, which_nz_out)
  assert not tangents_stack
  return tracers_out

