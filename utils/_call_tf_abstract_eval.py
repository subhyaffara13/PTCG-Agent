
def _call_tf_abstract_eval(
    *args_flat_avals,
    function_flat_tf,
    args_flat_sig_tf,
    has_side_effects,
    ordered,
    output_avals,
    call_tf_graph,
    **__,
):
  # Called only when we form a Jaxpr, i.e., under jit, scan, etc.
  effs: set[effects.Effect] = set()
  if ordered:
    effs.add(call_tf_ordered_effect)
  elif has_side_effects:
    effs.add(call_tf_effect)

  # If no output_avals is given, then we ask TF to infer the output shapes.
  # We call this even if output_avals is given because it will ensure that
  # callable_flat_tf is called. Since _get_concrete_function_tf is cached
  # there is a small cost of calling it more often than needed.
  concrete_function_flat_tf = _get_concrete_function_tf(function_flat_tf,
                                                        args_flat_sig_tf)

  # In the case that the tf.function has no return value
  if len(concrete_function_flat_tf.outputs) == 0:
    return (), effs

  if output_avals is not None:
    return output_avals, effs

  def is_fully_known_shape(s):
    return s.rank is not None and all(d is not None for d in s)

  if all(is_fully_known_shape(s)
        for s in concrete_function_flat_tf.output_shapes):
    avals_from_tf = tuple(
        # We convert to JAX type, and canonicalize to 32-bit if necessary
        core.ShapedArray(shape, jax2tf_internal._to_jax_dtype(dtype))
        for dtype, shape in zip(concrete_function_flat_tf.output_dtypes,
                                concrete_function_flat_tf.output_shapes))
    return avals_from_tf, effs

  msg = ("call_tf cannot call functions whose output has dynamic shape. "
    f"Found output shapes: {concrete_function_flat_tf.output_shapes}. "
    "Consider using the `output_shape_dtype` argument to call_tf. "
    "\nSee https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#limitations-of-call_tf"
      " for a discussion.")
  raise ValueError(msg)

