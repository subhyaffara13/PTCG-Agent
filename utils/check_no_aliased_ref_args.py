
def check_no_aliased_ref_args(dbg_fn: Callable[[], core.DebugInfo],
                              maybe_avals, args) -> None:
  assert config.mutable_array_checks.value
  refs: dict[int, int] = {}
  for i, (a, x) in enumerate(zip(maybe_avals, args)):
    if (isinstance(a, AbstractRef) and
        (dup_idx := refs.setdefault(id(core.get_referent(x)), i)) != i):
      dbg = dbg_fn()
      raise ValueError(
        "only one reference to a mutable array may be passed as an argument "
        f"to a function, but when tracing {dbg.func_src_info} for {dbg.traced_for} "
        f"the mutable array reference of type {a.str_short()} appeared at both "
        f"{dbg.arg_names[dup_idx] if dbg.arg_names is not None else 'unknown'} "
        f"and {dbg.arg_names[i] if dbg.arg_names is not None else 'unknown'}."
        if dbg else
        f"at both flat index {dup_idx} and flat index {i}") from None

