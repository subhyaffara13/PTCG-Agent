
def _infer_input_type(fun: Callable, dbg_fn: Callable[[], core.DebugInfo],
                      explicit_args) -> tuple[core.AbstractValue, ...]:
  avals = []
  i = -1
  x = None
  try:
    for i, x in enumerate(explicit_args):
      avals.append(core.shaped_abstractify(x))
  except OverflowError:
    dbg = dbg_fn()
    arg_path = f"argument path is {dbg.arg_names[i] if dbg.arg_names is not None else 'unknown'}"
    raise OverflowError(
      "An overflow was encountered while parsing an argument to a jitted "
      f"computation, whose {arg_path}. Got {type(x)} with value {x}"
    ) from None
  except TypeError:
    dbg = dbg_fn()
    arg_description = f"path {dbg.arg_names[i] if dbg.arg_names is not None else 'unknown'}"
    raise TypeError(
      f"Error interpreting argument to {fun} as an abstract array."
      f" The problematic value is of type {type(x)} and was passed to"
      f" the function at {arg_description}.\n"
      "This typically means that a jit-wrapped function was called with a non-array"
      " argument, and this argument was not marked as static using the"
      " static_argnums or static_argnames parameters of jax.jit."
    ) from None
  if config.mutable_array_checks.value:
    check_no_aliased_ref_args(dbg_fn, avals, explicit_args)
  return tuple(avals)

