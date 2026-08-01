
def estimate_cost(fun, *args, **kwargs) -> pallas_core.CostEstimate:
  """Computes a cost estimate for the given function.

  Args:
    fun: The function to compute the cost estimate for.
    *args: The arguments to the function. Can be jax.ShapeDtypeStruct or
      jax.Array.
    **kwargs: The keyword arguments to the function.

  Returns:
    A pallas_core.CostEstimate object containing the cost estimate.
  """
  flattened_args, treedef = tree_util.tree_flatten(args)
  partial_fun = functools.partial(fun, **kwargs)
  wrapped_fun, _ = api_util.flatten_fun_nokwargs(
      lu.wrap_init(partial_fun,
                   debug_info=api_util.debug_info("cost_estimate", fun,
                                                  args, {})),
      treedef)
  avals = [jax_core.ShapedArray(a.shape, a.dtype) for a in flattened_args]
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, avals)
  estimate = cost_estimate_jaxpr(jax_core.ClosedJaxpr(jaxpr, consts))
  input_bytes = sum(
      math.prod(a.shape) * a.dtype.itemsize for a in flattened_args)
  output_bytes = sum(
      math.prod(a.aval.shape) * a.aval.dtype.itemsize for a in jaxpr.outvars)
  return pallas_core.CostEstimate(
      flops=estimate.flops,
      transcendentals=estimate.transcendentals,
      bytes_accessed=estimate.bytes_accessed + input_bytes + output_bytes,
  )

