
def _pjit_call_impl(*args, jaxpr: core.ClosedJaxpr,
                    in_shardings, out_shardings, in_layouts, out_layouts,
                    donated_invars, ctx_mesh, name, keep_unused, inline,
                    compiler_options_kvs):
  def call_impl_cache_miss(*args_, **kwargs_):
    # args_ do not include the const args
    # See https://docs.jax.dev/en/latest/internals/constants.html.
    # TODO(necula): remove num_const_args when fixing the C++ path
    out_flat, compiled, pgle_profiler, const_args = _pjit_call_impl_python(
        *args, jaxpr=jaxpr, in_shardings=in_shardings,
        out_shardings=out_shardings, in_layouts=in_layouts,
        out_layouts=out_layouts, donated_invars=donated_invars,
        ctx_mesh=ctx_mesh, name=name, keep_unused=keep_unused,
        inline=inline, compiler_options_kvs=compiler_options_kvs)
    fastpath_data = _get_fastpath_data(
        compiled, tree_structure(out_flat), args, out_flat,
        jaxpr.effects, jaxpr.consts, pgle_profiler,
        const_args)
    return out_flat, fastpath_data, _need_to_rebuild_with_fdo(pgle_profiler)

  f = _get_jaxpr_as_fun(
      jaxpr, in_shardings, out_shardings, in_layouts, out_layouts,
      donated_invars, ctx_mesh, name, keep_unused, inline,
      compiler_options_kvs)
  donated_argnums = tuple(i for i, d in enumerate(donated_invars) if d)
  cache_key = pxla.JitGlobalCppCacheKeys(
      donate_argnums=donated_argnums, donate_argnames=None,
      device=None, backend=None,
      in_shardings_treedef=None, in_shardings_leaves=in_shardings,
      out_shardings_treedef=None, out_shardings_leaves=out_shardings,
      in_layouts_treedef=None, in_layouts_leaves=in_layouts,
      out_layouts_treedef=None, out_layouts_leaves=out_layouts)
  return _jax.pjit(
      name, f, call_impl_cache_miss, [], [], cache_key,
      tree_util.dispatch_registry, pxla.cc_shard_arg,
      _get_cpp_global_cache(cache_key.contains_explicit_attributes))(*args)

