
def _pjit_jvp(primals_in, tangents_in,
              jaxpr, in_shardings, out_shardings, in_layouts, out_layouts,
              donated_invars, ctx_mesh, name, keep_unused, inline,
              compiler_options_kvs):
  is_nz_tangents_in = [type(t) is not ad.Zero for t in tangents_in]
  jaxpr_jvp, is_nz_tangents_out = ad.jvp_jaxpr(
      jaxpr, is_nz_tangents_in, instantiate=False)

  def _filter_zeros(is_nz_l, l):
    return (x for nz, x in zip(is_nz_l, l) if nz)
  _filter_zeros_in = partial(_filter_zeros, is_nz_tangents_in)
  _filter_zeros_out = partial(_filter_zeros, is_nz_tangents_out)
  outputs = jit_p.bind(
      *primals_in, *_filter_zeros_in(tangents_in),
      jaxpr=jaxpr_jvp,
      in_shardings=(*in_shardings, *_filter_zeros_in(in_shardings)),
      out_shardings=(*out_shardings, *_filter_zeros_out(out_shardings)),
      in_layouts=(*in_layouts, *_filter_zeros_in(in_layouts)),
      out_layouts=(*out_layouts, *_filter_zeros_out(out_layouts)),
      donated_invars=(*donated_invars, *_filter_zeros_in(donated_invars)),
      ctx_mesh=ctx_mesh,
      name=name,
      keep_unused=keep_unused,
      inline=inline,
      compiler_options_kvs=compiler_options_kvs)

  primals_out, tangents_out = split_list(outputs, [len(jaxpr.jaxpr.outvars)])
  assert len(primals_out) == len(jaxpr.jaxpr.outvars)
  tangents_out_it = iter(tangents_out)
  return primals_out, [next(tangents_out_it) if nz else ad.Zero(aval)
                       for nz, aval in zip(is_nz_tangents_out, jaxpr.out_avals)]

