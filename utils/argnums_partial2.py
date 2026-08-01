
def argnums_partial2(f: Callable, dyn_argnums: int | Sequence[int],
                     args: Sequence, kwargs: dict):
  # like argnums_partial but works with callables instead of WrappedFun
  dyn_argnums = _ensure_index_tuple(dyn_argnums)
  dyn_argnums = _ensure_inbounds(False, len(args), dyn_argnums)
  static_args = list(args)
  dyn_args = []
  for i in dyn_argnums:
    x = static_args[i]
    dyn_args.append(x)
    static_args[i] = None

  def f_wrapped(*dyn_args_):
    args_ = list(static_args)
    for i, x in zip(dyn_argnums, dyn_args_):
      args_[i] = x
    return f(*args_, **kwargs)

  return f_wrapped, tuple(dyn_args)

