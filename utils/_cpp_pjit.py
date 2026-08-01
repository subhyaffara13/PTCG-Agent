
def _cpp_pjit(fun: Callable, jit_info: PjitInfo):

  @api_boundary
  def cache_miss(*args, **kwargs):
    # args do not include the const args
    # See https://docs.jax.dev/en/latest/internals/constants.html.
    if config.no_tracing.value:
      raise RuntimeError(f"re-tracing function {jit_info.fun_sourceinfo} for "
                         "`jit`, but 'no_tracing' is set")
    p, args_flat = _infer_params(fun, jit_info, args, kwargs)
    (outs, out_flat, out_tree, args_flat, jaxpr,
     executable, pgle_profiler, const_args) = _run_python_pjit(
         p, args_flat, fun, args, kwargs)

    maybe_fastpath_data = _get_fastpath_data(
        executable, out_tree, args_flat, out_flat, jaxpr.effects, jaxpr.consts,
        pgle_profiler, const_args)

    return outs, maybe_fastpath_data, _need_to_rebuild_with_fdo(pgle_profiler)

  cache_key = pxla.JitGlobalCppCacheKeys(
      donate_argnums=jit_info.donate_argnums,
      donate_argnames=jit_info.donate_argnames,
      device=jit_info.device, backend=jit_info.backend,
      in_shardings_treedef=jit_info.in_shardings_treedef,
      in_shardings_leaves=jit_info.in_shardings_leaves,
      out_shardings_treedef=jit_info.out_shardings_treedef,
      out_shardings_leaves=jit_info.out_shardings_leaves,
      in_layouts_treedef=jit_info.in_layouts_treedef,
      in_layouts_leaves=jit_info.in_layouts_leaves,
      out_layouts_treedef=jit_info.out_layouts_treedef,
      out_layouts_leaves=jit_info.out_layouts_leaves,
      compiler_options_kvs=jit_info.compiler_options_kvs)

  cpp_cache = (cache
               if ((cache := config.jax_jit_cpp_cache_obj.value) is not None
                   and core.trace_state_clean())
               else _get_cpp_global_cache(cache_key.contains_explicit_attributes))

  cpp_pjit_f = _jax.pjit(
      fun_name(fun), fun, cache_miss, jit_info.static_argnums,
      jit_info.static_argnames, cache_key, tree_util.dispatch_registry,
      pxla.cc_shard_arg, cpp_cache)

  cpp_pjitted_f = wraps(fun)(cpp_pjit_f)
  cpp_pjitted_f._fun = fun  # pyrefly: ignore[missing-attribute]
  cpp_pjitted_f._jit_info = jit_info  # pyrefly: ignore[missing-attribute]
  cpp_jitted_f_class = type(cpp_pjitted_f)
  cpp_jitted_f_class.clear_cache = jit_evict_fn
  cpp_jitted_f_class.lower = jit_lower
  cpp_jitted_f_class.trace = jit_trace
  cpp_jitted_f_class.eval_shape = jit_eval_shape
  return cpp_pjitted_f

