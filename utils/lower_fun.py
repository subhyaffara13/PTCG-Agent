
def lower_fun(fun: Callable, multiple_results: bool = True) -> Callable:
  """Converts a traceable JAX function `fun` into a lowering rule.

  The returned function does not use `avals_out`, so callers may pass any value
  as `avals_out`."""
  def f_lowered(ctx: LoweringRuleContext, *args, **params):
    f = fun if multiple_results else lambda *args, **kw: (fun(*args, **kw),)
    wrapped_fun = lu.wrap_init(f, params,
        debug_info=api_util.debug_info("lower_fun", fun, args, {}))

    jaxpr, _, consts_for_constvars = pe.trace_to_jaxpr_dynamic(
        wrapped_fun, ctx.avals_in, lower=True)

    if any(isinstance(e, core.InternalMutableArrayEffect) for e in jaxpr.effects):
      from jax._src.interpreters import pxla  # pyrefly: ignore[missing-module-attribute]
      closed_jaxpr = core.ClosedJaxpr(jaxpr, consts_for_constvars)
      closed_jaxpr = pxla._discharge_internal_refs(closed_jaxpr)
      jaxpr, consts_for_constvars = closed_jaxpr.jaxpr, closed_jaxpr.consts

    # TODO(frostig,mattjj): check ctx.avals_out against jaxpr avals out?

    if ctx.platforms is not None:
      sub_context = ctx.module_context.replace(platforms=ctx.platforms)
    else:
      sub_context = ctx.module_context
    out, tokens = jaxpr_subcomp(
        sub_context, jaxpr, ctx.name_stack, ctx.tokens_in,
        ir_consts(consts_for_constvars, [v.aval for v in jaxpr.constvars]),
        *args,
        dim_var_values=ctx.dim_var_values,
        const_lowering=ctx.const_lowering,
        outer_traceback=xc.Traceback())
    ctx.set_tokens_out(tokens)
    return out

  return f_lowered


def lower_fun(
    fun: Callable,
    *,
    in_avals: Any | None = None,
) -> Callable:
  """Converts a traceable JAX function `fun` into a lowering rule.

  Can handle PyTree arguments if `in_avals` is provided dynamically, otherwise
  assumes flat arguments matching `ctx.avals_in`.
  """

  def f_lowered(ctx: LoweringRuleContext, *args, **params):
    flat_args, in_tree = tree_util.tree_flatten(args)
    if in_avals is None:
      flat_avals = ctx.avals_in
      sub_block_shapes = ctx.block_shapes
    else:
      flat_avals, aval_tree = tree_util.tree_flatten(in_avals)
      if in_tree != aval_tree:
        raise ValueError(
            "args and in_avals pytrees mismatch:\\nargs tree:"
            f" {in_tree}\\navals tree: {aval_tree}\\nargs: {args}\\navals:"
            f" {in_avals}"
        )
      sub_block_shapes = [None] * len(flat_args)
    wrapped_lu_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
        lu.wrap_init(
            fun,
            params,
            debug_info=api_util.debug_info("mosaic lower_fun", fun, args, {}),
        ),
        in_tree,
    )
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_lu_fun, flat_avals, lower=True)
    if consts:
      raise NotImplementedError("lower_fun should not capture constvars")
    jaxpr = pe.convert_constvars_jaxpr(jaxpr)
    sub_lowering_ctx = ctx.lowering_context.replace(
        block_shapes=sub_block_shapes
    )
    out = jaxpr_subcomp(sub_lowering_ctx, jaxpr, *consts, *flat_args)
    return tree_util.tree_unflatten(out_tree_thunk(), out)

  return f_lowered


def lower_fun(
    fun: Callable[..., Any], *, multiple_results: bool
) -> Callable[..., Any]:
  fn = fun if multiple_results else lambda *args, **kw: (fun(*args, **kw),)

  def f_lowered(ctx: LoweringRuleContext, *args, **params):
    wrapped_fun = lu.wrap_init(
        fn, params,
        debug_info=api_util.debug_info("pallas triton lower_fun", fun,
                                       args, params))
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, ctx.avals_in, lower=True)
    jaxpr = jax_core.ClosedJaxpr(jaxpr, consts)
    out = _closed_call_lowering_rule(ctx, *args, call_jaxpr=jaxpr)
    return out if multiple_results else out[0]

  return f_lowered

