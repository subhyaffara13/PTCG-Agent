
def _check_tree_and_avals(what1, tree1, avals1, what2, tree2, avals2):
  """Raises TypeError if (tree1, avals1) does not match (tree2, avals2).

  Corresponding `tree` and `avals` must match in the sense that the number of
  leaves in `tree` must be equal to the length of `avals`. `what1` and
  `what2` describe what the `tree1` and `tree2` represent.
  """
  if tree1 != tree2:
    errs = list(equality_errors_pytreedef(tree1, tree2))
    msg = []
    msg.append(
        f"{what1} must have same type structure as {what2}, but there are differences: ")
    for path, thing1, thing2, explanation in errs:
      msg.append(
          f"    * at output{keystr(tuple(path))}, {what1} has {thing1} and "
          f"{what2} has {thing2}, so {explanation}")
    raise TypeError('\n'.join(msg))

  if not all(map(core.typematch, avals1, avals2)):
    diff = tree_map(_show_diff, tree_unflatten(tree1, avals1),
                    tree_unflatten(tree2, avals2))
    raise TypeError(f"{what1} and {what2} must have identical types, got\n{diff}.")

