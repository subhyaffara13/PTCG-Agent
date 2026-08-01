
def _infer_params(
    fun: Callable, ji: PjitInfo, args: tuple[Any, ...], kwargs: dict[str, Any]
  ) -> tuple[PjitParams, list[core.Value]]:
  ctx_mesh = get_ctx_mesh(ji.use_resource_env)
  dbg_fn = lambda: debug_info(
      'jit', fun, args, kwargs, static_argnums=ji.static_argnums,
      static_argnames=ji.static_argnames, sourceinfo=ji.fun_sourceinfo,
      signature=ji.fun_signature)
  arg_signature, dynargs = jax_jit.parse_arguments(
      args, tuple(kwargs.values()), tuple(kwargs.keys()), ji.static_argnums,
      ji.static_argnames, tree_util.tracing_registry)
  avals = _infer_input_type(fun, dbg_fn, dynargs)
  entry = _infer_params_cached(fun, ji, arg_signature, avals, ctx_mesh)

  if entry.pjit_params is not None:
    return entry.pjit_params, entry.pjit_params.consts + dynargs

  p = _trace_for_jit(fun, ji, ctx_mesh, dbg_fn(), avals, args, kwargs)
  if p.params['jaxpr'].jaxpr.is_high:
    return p, p.consts + dynargs
  entry.pjit_params = p
  return p, p.consts + dynargs

