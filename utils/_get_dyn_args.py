
def _get_dyn_args(wrapped_f, static_broadcasted_tuple, args):
  """Extract dynamic args and argnums after handling static args.

  Args:
    wrapped_f: The wrapped function.
    static_broadcasted_tuple: Tuple of static argument indices.
    args: Positional arguments.

  Returns:
    dyn_f: function with static args bound
    dyn_argnums: list of dynamic arg indices (or None if no static args)
    dyn_args: dynamic positional arguments (after static removed)

  Raises:
    ValueError: If static_broadcasted_argnums exceeds number of args.
  """

  if static_broadcasted_tuple:
    if max(static_broadcasted_tuple) >= len(args):
      raise ValueError(
          "pmapped function has"
          f" static_broadcasted_argnums={static_broadcasted_tuple} but was"
          f" called with only {len(args)} positional"
          f" argument{'s' if len(args) > 1 else ''}. All static broadcasted"
          " arguments must be passed positionally."
      )
    dyn_argnums = [
        i for i in range(len(args)) if i not in static_broadcasted_tuple
    ]
    wrapped_f, dyn_args = argnums_partial(wrapped_f, dyn_argnums, args)
  else:
    dyn_argnums = None
    dyn_args = args
  return wrapped_f, dyn_argnums, dyn_args

