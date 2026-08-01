
def pytreedef_mismatch_err_msg(
    what1: str, tree1: tree_util.PyTreeDef,
    what2: str, tree2: tree_util.PyTreeDef) -> str:
  errs = list(tree_util.equality_errors_pytreedef(tree1, tree2))
  msg = []
  msg.append(
      f"Pytree for {what1} and {what2} do not match. "
      f"There are {len(errs)} mismatches, including:")
  for path, thing1, thing2, explanation in errs:
    where = f"at {tree_util.keystr(path)}, " if path else ""
    msg.append(
        f"    * {where}{what1} is a {thing1} but"
        f" {what2} is a {thing2}, so {explanation}")
  return "\n".join(msg)

