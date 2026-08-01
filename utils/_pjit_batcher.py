
def _pjit_batcher(axis_data, vals_in,
                  dims_in: tuple[int, ...],
                  jaxpr: core.ClosedJaxpr,
                  in_shardings, out_shardings, in_layouts, out_layouts,
                  donated_invars, ctx_mesh, name, keep_unused, inline,
                  compiler_options_kvs):
  new_jaxpr, axes_out = batching.batch_jaxpr2(jaxpr, axis_data, dims_in)
  in_shardings = tuple(
      _pjit_batcher_for_sharding(i, axis_in, axis_data.spmd_name, ctx_mesh,
                                 aval.ndim)
      if axis_in is not None else i
      for axis_in, i, aval in zip(dims_in, in_shardings, new_jaxpr.in_avals))
  out_shardings = tuple(

      _pjit_batcher_for_sharding(o, axis_out, axis_data.spmd_name, ctx_mesh,
                                 aval.ndim)
      if axis_out is not None else o
      for axis_out, o, aval in zip(axes_out, out_shardings, new_jaxpr.out_avals))
  # TODO(yashkatariya): Figure out layouts should change under vmap.
  if not (all(l is None for l in in_layouts) and
          all(l is None for l in out_layouts)):
    raise NotImplementedError(
        'Concrete layouts are not supported for vmap(jit).')

  vals_out = jit_p.bind(
    *vals_in,
    jaxpr=new_jaxpr,
    in_shardings=in_shardings,
    out_shardings=out_shardings,
    in_layouts=in_layouts,
    out_layouts=out_layouts,
    donated_invars=donated_invars,
    ctx_mesh=ctx_mesh,
    name=name,
    keep_unused=keep_unused,
    inline=inline,
    compiler_options_kvs=compiler_options_kvs)

  return vals_out, axes_out

