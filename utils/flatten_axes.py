
def flatten_axes(axes: Axes | Iterable[Axes]) -> Generator[Axes]:
    if not is_list_like(axes):
        yield axes  # type: ignore[misc]
    elif isinstance(axes, (np.ndarray, ABCIndex)):
        yield from np.asarray(axes).reshape(-1)
    else:
        yield from axes  # type: ignore[misc]


def flatten_axes(name, treedef, axis_tree, *, kws=False, tupled_args=False):
  # given an axis spec tree axis_tree (a pytree with integers and Nones at the
  # leaves, i.e. the Nones are to be considered leaves) that is a tree prefix of
  # the given treedef, build a complete axis spec tree with the same structure
  # and return the flattened result
  axis_tree_leaves, axis_treedef = none_leaf_registry.flatten(axis_tree)
  try:
    axes = broadcast_flattened_prefix_with_treedef(
        axis_tree_leaves, axis_treedef, treedef)
  except ValueError:
    if kws:
      # if keyword arguments are included in the tree, we make adapt the error
      # message only to be about the positional arguments
      treedef, _ = treedef_children(treedef)
      axis_tree, _ = axis_tree
    hint = ""
    if tupled_args:
      hint += (f" Note that {name} that are non-trivial pytrees should always be "
               f"wrapped in a tuple representing the argument list.")
      if len(treedef.children()) == 1:
        try:
          flatten_axes(name, treedef, (axis_tree,))
        except ValueError:
          pass  # That's not the issue.
        else:
          hint += (f" In particular, you're passing in a single argument which "
                   f"means that {name} might need to be wrapped in "
                   f"a singleton tuple.")
    dummy_tree = tree_unflatten(treedef, [PytreeLeaf()] * treedef.num_leaves)
    errors = prefix_errors(axis_tree, dummy_tree)
    if errors:
      details = "\n  ".join(e(name).args[0] for e in errors)
      prefix_err_msg = (
          f"\n  Mismatch details ({len(errors)} found):\n  {details}")
      raise ValueError(
          f"{name} specification must be a tree prefix of the "
          f"corresponding value; {hint}{prefix_err_msg}") from None
    # At this point we've failed to find a tree prefix error.
    assert False, "unreachable code"
  assert len(axes) == treedef.num_leaves
  return axes

