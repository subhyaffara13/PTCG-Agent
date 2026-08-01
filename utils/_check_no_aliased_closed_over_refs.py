
def _check_no_aliased_closed_over_refs(dbg: core.DebugInfo, consts, args) -> None:
  assert config.mutable_array_checks.value
  refs: set[int] = {id(core.get_referent(c)) for c in consts
                    if isinstance(core.typeof(c), AbstractRef)}
  for i, x in enumerate(args):
    if id(core.get_referent(x)) in refs:
      a = core.shaped_abstractify(x)
      raise ValueError(
          f"when tracing {dbg.func_src_info} for {dbg.traced_for}, a mutable "
          f"array reference of type {a.str_short()} was both closed over and "
          f"passed as the argument "
          f"{dbg.safe_arg_names(len(args))[i]}" if dbg else "at flat index {i}")

