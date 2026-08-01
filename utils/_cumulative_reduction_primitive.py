
def _cumulative_reduction_primitive(name, reduce_fn, reduce_window_fn):
  reducer_p = lax.standard_primitive(
    _cumred_shape_rule, partial(_cumred_dtype_rule, name),
    name, sharding_rule=_cumred_sharding_rule,
    vma_rule=partial(core.standard_vma_rule, name))
  batching.primitive_batchers[reducer_p] = partial(_cumred_batch_rule,
                                                   reducer_p)

  def register_lowering(fn, platform=None):
    mlir.register_lowering(
        reducer_p,
        mlir.lower_fun(fn, multiple_results=False),
        platform=platform,
        inline=False)

  # In XLA, there's a rewriter for an O(N^2) reduce-window implementation.
  register_lowering(
      partial(cumred_reduce_window_impl, reduce_window_fn)
  )

  return reducer_p

