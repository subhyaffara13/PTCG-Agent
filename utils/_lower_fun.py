from typing import Any, Callable

def _lower_fun(
    fun: Callable,
    *,
    in_avals: Any | None = None,
) -> Callable:

  def f_lowered(ctx: LoweringRuleContext, *args, **params):
    is_leaf = lambda x: isinstance(
        x, (mgpu.FragmentedArray, mgpu.WGMMAAccumulator)
    )
    flat_args, in_tree = tree_util.tree_flatten(args, is_leaf=is_leaf)
    if in_avals is None:
      flat_avals = ctx.avals_in
    else:
      flat_avals, aval_tree = tree_util.tree_flatten(in_avals)
      if in_tree != aval_tree:
        raise ValueError(
            "args and in_avals pytrees mismatch:\nargs tree:"
            f" {in_tree}\navals tree: {aval_tree}\nargs: {args}\navals:"
            f" {in_avals}"
        )
    wrapped_lu_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
        lu.wrap_init(
            fun,
            params,
            debug_info=api_util.debug_info("mosaic_gpu lower_fun", fun, args, {}),
        ),
        in_tree,
    )
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_lu_fun, flat_avals, lower=True)
    if consts:
      raise NotImplementedError("lower_fun should not capture constvars")
    jaxpr = pe.convert_constvars_jaxpr(jaxpr)
    out = lower_jaxpr_to_mosaic_gpu(
        ctx.module_ctx, ctx.launch_ctx, jaxpr, flat_args, consts
    )
    return tree_util.tree_unflatten(out_tree_thunk(), out)

  return f_lowered

