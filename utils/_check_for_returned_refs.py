
def _check_for_returned_refs(f, out, kind, args, after_idx):
  args = [x.value if isinstance(x, CustomVJPPrimal) else x for x in args]
  ids = {id(x) for x in args if isinstance(core.typeof(x), AbstractRef)}
  leaves = tree_leaves_with_path(out)
  for i, (path, leaf) in enumerate(leaves):
    if isinstance((a := core.typeof(leaf)), AbstractRef):
      loc = f' at output tree path {keystr(path)}' if path else ''
      if i < after_idx:
        raise ValueError(f"custom_vjp {kind} function {f} returned a mutable "
                         f"array reference of type {a.str_short()}{loc}, "
                         "but mutable array references cannot be returned there.")
      if id(leaf) not in ids:
        raise ValueError(f"custom_vjp {kind} function {f} returned a mutable "
                         f"array reference of type {a.str_short()}{loc} "
                         "that was not an argument.")

