
def _check_for_aliased_refs(
    f: Callable, nondiff_argnums: Sequence[int], debug: core.DebugInfo, args):
  argnums = [x for i, arg in enumerate(args)
             for x in [i] * tree_structure(arg).num_leaves]
  leaves = tree_leaves(args)
  refs: dict[int, int] = {}
  for i, (argnum, x) in enumerate(zip(argnums, leaves)):
    if argnum in nondiff_argnums: continue
    x = x.value if isinstance(x, CustomVJPPrimal) else x
    if (isinstance((a := core.typeof(x)), AbstractRef) and
        (dup_idx := refs.setdefault(id(core.get_referent(x)), i)) != i):
      arg_names = debug.safe_arg_names(len(leaves))
      raise ValueError(
          "only one reference to a mutable array may be passed as an argument "
          f"to a function, but custom_vjp function {f} got the same mutable "
          f"array reference of type {a.str_short()} at {arg_names[dup_idx]} and"
          f" {arg_names[i]}.")

