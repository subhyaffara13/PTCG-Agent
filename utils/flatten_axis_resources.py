
def flatten_axis_resources(what, tree, shardings, tupled_args):
  try:
    return tuple(flatten_axes(what, tree, shardings, tupled_args=tupled_args))
  except ValueError:
    pass  # Raise a tree prefix error below

  # Tree leaves are always valid prefixes, so if there was a prefix error as
  # assumed here, axis_resources must not be a leaf.
  assert not treedef_is_leaf(tree_structure(shardings))

  # Check the type directly rather than using isinstance because of namedtuples.
  if tupled_args and (type(shardings) is not tuple or
                      len(shardings) != len(tree.children())):
    # We know axis_resources is meant to be a tuple corresponding to the args
    # tuple, but while it is a non-leaf pytree, either it wasn't a tuple or it
    # wasn't the right length.
    msg = (f"{what} specification must be a tree prefix of the positional "
           f"arguments tuple. In particular, {what} must either be a Sharding, "
           "a PartitionSpec, or a tuple of length equal to the number of "
           "positional arguments.")
    # If `tree` represents an args tuple, then `axis_resources` must be a tuple.
    # TODO(mattjj,apaszke): disable implicit list casts, remove 'or list' below
    if type(shardings) is not tuple:
      msg += f" But {what} is not a tuple: got {type(shardings)} instead."
    elif len(shardings) != len(tree.children()):
      msg += (f" But {what} is the wrong length: got a tuple or list of length "
              f"{len(shardings)} for an args tuple of length "
              f"{len(tree.children())}.")

    # As an extra hint, let's check if the user just forgot to wrap
    # shardings in a singleton tuple.
    if len(tree.children()) == 1:
      try: flatten_axes(what, tree, (shardings,))
      except ValueError: pass  # That's not the issue.
      else:
        msg += (f" Given the corresponding argument being "
                f"passed, it looks like {what} might need to be wrapped in "
                f"a singleton tuple.")

    raise ValueError(msg)

  axis_tree = shardings

  # Because we only have the `tree` treedef and not the full pytree here,
  # we construct a dummy tree to compare against. Revise this in callers?
  dummy_tree = tree_unflatten(tree, [PytreeLeaf()] * tree.num_leaves)
  errors = prefix_errors(axis_tree, dummy_tree)
  if errors:
    details = "\n".join(e(what).args[0] for e in errors)
    raise ValueError(
        f"Mismatch details ({len(errors)} found):\n{details}"
    )

  # At this point we've failed to find a tree prefix error.
  assert False, "Please open a bug report!"  # This should be unreachable.

