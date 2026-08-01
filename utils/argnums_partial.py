
def argnums_partial(f: lu.WrappedFun, dyn_argnums: int | Sequence[int],
                    args: Sequence, require_static_args_hashable=True):
  dyn_argnums = _ensure_index_tuple(dyn_argnums)
  dyn_argnums = _ensure_inbounds(False, len(args), dyn_argnums)
  fixed_args: list
  if require_static_args_hashable:
    fixed_args = []
    for i, arg in enumerate(args):
      if i in dyn_argnums: continue
      if not is_hashable(arg):
        raise ValueError(
            "Non-hashable static arguments are not supported, as this can lead "
            f"to unexpected cache-misses. Static argument (index {i}) of type "
            f"{type(arg)} for function {f.__name__} is non-hashable.")
      fixed_args.append(_HashableWithStrictTypeEquality(arg))
  else:
    fixed_args = [Unhashable(arg) for i, arg in enumerate(args)
                  if i not in dyn_argnums]
  dyn_args = tuple(args[i] for i in dyn_argnums)
  return _argnums_partial(f, dyn_argnums, tuple(fixed_args)), dyn_args

