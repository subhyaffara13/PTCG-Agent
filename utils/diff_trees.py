
def diff_trees(new_tree, old_tree) -> tuple[int, int, str] | None:
  errs = tree_util.equality_errors_pytreedef(new_tree, old_tree)
  tree_diffs = []
  for path, thing1, thing2, explanation in errs:
    tree_diffs.append(
        f"  * at input path {tree_util.keystr(tuple(path))}, now {thing1} and "
        f"before {thing2}, so {explanation}")
  msg = 'different input pytree:\n' + '\n'.join(tree_diffs)
  if tree_diffs: return 1, len(tree_diffs), msg

