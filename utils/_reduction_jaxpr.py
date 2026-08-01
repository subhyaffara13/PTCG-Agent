
def _reduction_jaxpr(computation: Callable,
                     aval: core.AbstractValue):
  def comp(x, y):
    result = computation(x, y)
    if not core.valid_jaxtype(result):
      raise ValueError(
          f"Invalid return type from reduction function: {type(result)}\n"
          f"Reduction functions should only return an array.\n"
          f"Full return value: {result}")
    return (result,)
  dbg = api_util.debug_info('reduction_jaxpr', computation, (aval, aval), {})
  closed_jaxpr, _ = pe.trace_to_jaxpr(
      comp, tree_util.FlatTree.flatten_args(aval, aval), dbg
  )
  if any(isinstance(c, core.Tracer) for c in closed_jaxpr.consts):
    raise NotImplementedError(
        "Reduction computations can't close over Tracers. Please open an issue "
        "at https://github.com/jax-ml/jax.")
  return closed_jaxpr.jaxpr, tuple(closed_jaxpr.consts)

