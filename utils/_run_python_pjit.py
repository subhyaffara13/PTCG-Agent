
def _run_python_pjit(p, args_flat, fun: Callable, args, kwargs):
  for arg in args_flat:
    dispatch.check_arg(arg)

  try:
    if (core.trace_state_clean() and not config.debug_key_reuse.value
        and not p.params['jaxpr'].jaxpr.is_high):
      args_flat = map(core.full_lower, args_flat)
      core.check_eval_args(args_flat)
      out_flat, compiled, profiler, const_args = _pjit_call_impl_python(
          *args_flat, **p.params)
    else:
      out_flat = jit_p.bind(*args_flat, **p.params)
      compiled = None
      profiler = None
      const_args = []
  except stages.DeviceAssignmentMismatchError as e:
    fails, = e.args
    fun_name = getattr(fun, '__qualname__', getattr(fun, '__name__', str(fun)))
    arg_types = map(convert_to_metaty, args_flat)
    msg = stages._device_assignment_mismatch_error(
        fun_name, fails, arg_types, 'jit', p.arg_names)
    raise ValueError(msg) from None
  except dtypes.InvalidInputException as e:
    arg_names = [''] * len(args_flat) if p.arg_names is None else p.arg_names
    # Run canonicalization again to figure out which arg failed.
    if p.params['jaxpr'].consts:
      raise TypeError(e.args[0]) from e
    else:
      for arg, name, aval in zip(args_flat, arg_names, p.in_avals):
        try:
          val = dtypes.canonicalize_value(arg)
          if type(val) not in pxla.shard_arg_handlers:
            raise dtypes.InvalidInputException(
                f"Argument '{name}' of type {type(arg)} is not a valid JAX type.")
        except dtypes.InvalidInputException as _:
          # Reraise as TypeError with the new message.
          raise TypeError(
              f"Argument '{name}' of shape {aval.str_short()} of type"
              f' {type(arg)} is not a valid JAX type.') from e
      raise AssertionError("Unreachable") from e
  except api_util.InternalFloatingPointError as e:
    if getattr(fun, '_apply_primitive', False):
      raise FloatingPointError(
          f"invalid value ({e.ty}) encountered in {fun.__qualname__}") from None
    api_util.maybe_recursive_nan_check(e, fun, args, kwargs)  # should always raise.
    raise RuntimeError("Internal error") from e  # fall-back error to be safe.

  outs = tree_unflatten(p.out_tree, out_flat)
  return (outs, out_flat, p.out_tree, args_flat,
          p.params['jaxpr'], compiled, profiler, const_args)

