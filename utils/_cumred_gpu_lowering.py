
def _cumred_gpu_lowering(
    reduce_window_fn: Callable,
    reducer: Callable,
    identity: Callable,
    ctx,
    x,
    *,
    axis,
    reverse,
):
  if not _is_supported_cumred(ctx.avals_in[0], axis, reverse):
    fun = partial(cumred_reduce_window_impl, reduce_window_fn)
    return mlir.lower_fun(fun, multiple_results=False)(
        ctx, x, axis=axis, reverse=reverse
    )
  return _cumred_chlo_lowering(
      ctx, x, axis=axis, reverse=reverse, reducer=reducer, identity=identity
  )

