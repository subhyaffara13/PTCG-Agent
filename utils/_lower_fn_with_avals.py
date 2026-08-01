
def _lower_fn_with_avals(f, avals_in):
  def inner(ctx, *args):
    f_ = lu.wrap_init(
        f,
        debug_info=api_util.debug_info(
            "Pallas Mosaic GPU lower_fn_with_avals", f, ("",) * len(args), {}
        ).with_unknown_names(),
    )
    flat_args, in_tree_ = tree_util.tree_flatten(args)
    flat_avals, in_tree = tree_util.tree_flatten(avals_in)
    fun, out_tree_thunk = api_util.flatten_fun_nokwargs(f_, in_tree)
    jaxpr, out_avals, consts = pe.trace_to_jaxpr_dynamic(fun, flat_avals, lower=True)
    out_tree = out_tree_thunk()
    out_flat = lower_jaxpr_to_mosaic_gpu(
        ctx.module_ctx, ctx.launch_ctx, jaxpr, flat_args, consts
    )

    return out_tree.unflatten(out_flat), out_tree.unflatten(out_avals)
  return inner

