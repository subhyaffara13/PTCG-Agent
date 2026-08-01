
def check_no_transformed_refs_args(dbg_fn: Callable[[], core.DebugInfo],
                                   args_flat) -> None:
  from jax._src.state.types import TransformedRef
  for i, arg in enumerate(args_flat):
    if isinstance(arg, TransformedRef):
      dbg = dbg_fn()
      raise TypeError(
        f"When tracing {dbg.func_src_info} for {dbg.traced_for}, "
        "TransformedRefs are not allowed, but got a TransformedRef with name "
        f"{dbg.arg_names[i] if dbg.arg_names is not None else 'unknown'}."
        if dbg else
        "TransformedRefs are not allowed in this context.") from None

