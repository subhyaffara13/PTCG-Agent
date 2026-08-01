
def partial_eval_by_shape(fn, input_spec, *args, **kwargs):
  """Lazily evaluate a function by using the shapes of the inputs.

  This function is similar to ``jax.eval_shape`` with the key difference that
  function outputs that can be computed without a concrete value of the
  inputs are returned as is instead of only the shape. See for example
  ``module.init_by_shape`` where this functionality is used to initialize a
  model without using input data lr computation.

  Args:
    fn: the function to be lazily evaluated.
    input_spec: an iterable of shapes or (shape, dtype) tuples specifying the
      shape and type of the inputs. If unspecified the dtype is float32.
    *args: other arguments passed to the module's apply function
    **kwargs: keyword arguments passed to the module's apply function
  Returns:
    A pair consisting of the model output and an instance of Model
  """
  # output cannot be returned in lazy_create because jax.eval_shape will only
  # return the shape and dtype.
  # TODO(mattjj,jheek): use a public JAX API
  f = lambda *inputs: fn(*inputs, *args, **kwargs)
  input_structs = [_parse_spec(spec) for spec in input_spec]
  inputs_flat, in_tree = jax.tree_util.tree_flatten(input_structs)

  debug_info = jax.api_util.debug_info("flax partial_eval_by_shape", f,
                                        (in_tree,), {})
  f_flat, out_tree = jax.api_util.flatten_fun_nokwargs(
    lu.wrap_init(f, debug_info=debug_info), in_tree)
  in_pvals = [
    pe.PartialVal.unknown(core.ShapedArray(x.shape, x.dtype))
    for x in inputs_flat
  ]
  _, out_pvals, _ = pe.trace_to_jaxpr_nounits(f_flat, in_pvals)
  out_flat = [
    const if pv is None else jax.ShapeDtypeStruct(pv.shape, pv.dtype)
    for pv, const in out_pvals
  ]
  return jax.tree_util.tree_unflatten(out_tree(), out_flat)

