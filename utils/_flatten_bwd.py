from typing import Any, Callable

def _flatten_bwd(f: Callable,
                 in_tree: PyTreeDef,
                 in_avals: Sequence[core.AbstractValue],  # primal avals
                 out_trees: Callable[[], tuple[PyTreeDef, PyTreeDef, list[int | None]]],
                 *args):
  out_tree, res_tree, _ = out_trees()
  assert len(args) == res_tree.num_leaves + out_tree.num_leaves
  res, cts_out = split_list(args, [res_tree.num_leaves])
  py_res = tree_unflatten(res_tree, res)
  py_cts_out = tree_unflatten(out_tree, cts_out)
  py_cts_in = f(py_res, py_cts_out)
  if isinstance(py_cts_in, list) and len(py_cts_in) == len(treedef_children(in_tree)):
    py_cts_in = tuple(py_cts_in)
  # For each None in py_cts_in, indicating an argument for which the rule
  # produces no cotangent, we replace it with a pytree with the structure of the
  # corresponding subtree of in_tree and with leaves of a non-pytree sentinel
  # object, to be replaced with Nones in the final returned result.
  zero = object()  # non-pytree sentinel to replace Nones in py_cts_in
  dummy = tree_unflatten(in_tree, [object()] * in_tree.num_leaves)
  keypaths, _ = unzip2(tree_flatten_with_path(dummy)[0])
  cts_in_flat = []
  def append(x, d):
    num_leaves = len(tree_flatten(d)[0])
    if x is None and d is not None:
      cts_in_flat.extend([zero] * num_leaves)
    elif x is not None:
      cts_in_flat.extend([x] * num_leaves)
    return x
  try:
    if not isinstance(py_cts_in, tuple):
      raise ValueError
    tree_map(append, py_cts_in, dummy, is_leaf=lambda x: x is None)
  except ValueError:
    _, in_tree2 = tree_flatten(py_cts_in)
    msg = ("Custom VJP bwd rule must produce an output with the same container "
           "(pytree) structure as the args tuple of the primal function, "
           "and in particular must produce a tuple of length equal to the "
           "number of arguments to the primal function, but got bwd output "
           "structure {} for primal input structure {}.")
    raise TypeError(msg.format(in_tree2, in_tree)) from None
  results: list[Any] = []
  for kp, a, ct in zip(keypaths, in_avals, cts_in_flat):
    if ct is zero or getattr(a.to_ct_aval(), 'dtype') == dtypes.float0:
      results.append(Zero(a.to_ct_aval()))
    elif type(ct) is SymbolicZero:
      if not core.typecompat(a.to_ct_aval(), a_ := ct.aval):
        msg = ("Custom VJP bwd rule produced a SymbolicZero with a shape/dtype "
               "that does not match the corresponding input tangent shape/dtype: "
               f"at output{keystr(kp)} the SymbolicZero had shape/dtype "
               f"{a_.str_short()} while the "
               f"corresponding input had shape/dtype {a.str_short()}. "
               "Consider just returning a None here instead of a SymbolicZero "
               "object.")
        raise ValueError(msg)
      results.append(Zero(ct.aval))
    else:
      if (not config.disable_bwd_checks.value and
          not core.typecompat(a.to_ct_aval(), a_ := core.typeof(ct))
          and not _ref_typecompat(a.to_ct_aval(), a_)
          and not _temporary_dtype_exception(a.to_ct_aval(), a_)):
        msg = ("Custom VJP bwd rule must produce an output with the same "
               "type as the args tuple of the primal function, but at "
               f"output{keystr(kp)} the bwd rule produced an output of "
               f"type {a_.str_short()} corresponding "
               f"to an input of type {a.str_short()}"
               f"{core.aval_mismatch_extra(a, a_)}")
        raise ValueError(msg)
      results.append(ct)
  return results

