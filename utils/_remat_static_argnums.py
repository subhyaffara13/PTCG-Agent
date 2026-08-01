
def _remat_static_argnums(fun, static_argnums, args):
  if type(static_argnums) is int:
    static_argnums = (static_argnums,)
  elif not (type(static_argnums) is tuple and
            all(type(d) is int for d in static_argnums)):
    raise TypeError("the `static_argnums` argument to `jax.checkpoint` / "
                    "`jax.remat` must be an int, tuple of ints or, bool, but "
                    f"got value {static_argnums}")

  if not all(-len(args) <= d < len(args) for d in static_argnums):
    raise ValueError("the `static_argnums` argument to `jax.checkpoint` / "
                     "`jax.remat` can only take integer values greater than or "
                     "equal to `-len(args)` and less than `len(args)`, but got "
                     f"{static_argnums}, while `len(args)` = {len(args)}")

  if not static_argnums:
    return fun, args
  nargs = len(args)
  static_argnums_ = frozenset(d % len(args) for d in static_argnums)
  dyn_args, static_args = [], []
  for i, x in enumerate(args):
    if i in static_argnums_: static_args.append(WrapHashably(x))
    else: dyn_args.append(x)
  new_fun = _dyn_args_fun(fun, static_argnums_, tuple(static_args), nargs)
  return new_fun, dyn_args

