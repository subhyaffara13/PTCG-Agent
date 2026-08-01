
def _get_in_axes_flat(
    in_axes, dyn_argnums, dyn_args, kwargs, num_flat_args, in_tree
):
  """Compute flat in_axes tuple from in_axes prefix and args structure.

  Args:
    in_axes: The original in_axes specification.
    dyn_argnums: The indices of dynamic (non-static) positional args, or None if
      no static args.
    dyn_args: The dynamic positional args (after static args removed).
    kwargs: The keyword arguments.
    num_flat_args: Total number of flat args.
    in_tree: The PyTreeDef of (dyn_args, kwargs).

  Returns:
    Flat tuple of axis indices (int or None for each flat arg).

  Raises:
    ValueError: If in_axes is not a valid prefix of the args structure.
  """
  # Compute dyn_in_axes from in_axes and dyn_argnums
  if dyn_argnums is not None and isinstance(in_axes, tuple):
    dyn_in_axes = tuple(in_axes[i] for i in dyn_argnums)
  else:
    dyn_in_axes = in_axes

  # Fast path: avoid broadcast_prefix for common simple cases
  in_axes_flat = None

  if isinstance(dyn_in_axes, int):
    if dyn_in_axes == 0:
      # Most common case: all args mapped on axis 0, including kwargs (which also get 0)
      in_axes_flat = (0,) * num_flat_args
    elif not kwargs:
      # No kwargs: broadcast single in_axes to all positional leaves
      in_axes_flat = (dyn_in_axes,) * num_flat_args
  elif dyn_in_axes is None and not kwargs:
    # Unusual case: no mapping, no kwargs
    in_axes_flat = (None,) * num_flat_args
  elif (
      not kwargs
      and isinstance(dyn_in_axes, tuple)
      and all(isinstance(ax, int) or ax is None for ax in dyn_in_axes)
  ):
    # No kwargs: check if it's a simple flat tuple matching positional args
    if len(dyn_in_axes) == len(dyn_args) and num_flat_args == len(dyn_args):
      # Each positional arg is a leaf (no nested structure)
      in_axes_flat = dyn_in_axes

  # Slow path: use broadcast_flattened_prefix_with_treedef for complex cases
  if in_axes_flat is None:
    try:
      # Flatten in_axes prefix tree (treating None as leaf)
      flat_in_axes_prefix, in_axes_tree = tree_flatten(
          (dyn_in_axes, 0), is_leaf=lambda x: x is None
      )
      in_axes_flat = tuple(
          broadcast_flattened_prefix_with_treedef(
              flat_in_axes_prefix, in_axes_tree, in_tree
          )
      )
    except ValueError:
      e, *_ = prefix_errors((dyn_in_axes, 0), (dyn_args, kwargs))
      ex = e("pmap in_axes")
      (msg,) = ex.args
      msg += (
          "\n\nThe 'full pytree' here is the tuple of arguments passed "
          "positionally to the pmapped function, and the value of `in_axes` "
          "must be a tree prefix of that tuple. But it was not a prefix."
      )
      if kwargs:
        msg += (
            "\n\nWhen some arguments are passed by keyword to the pmapped "
            "function, they are not included in the comparison to `in_axes`. "
            "Instead, each argument passed by keyword is mapped over its "
            "leading axis. See the description of `in_axes` in the `pmap` "
            "docstring: "
            "https://docs.jax.dev/en/latest/_autosummary/jax.pmap.html#jax.pmap"
        )
      msg += (
          "\n\nCheck that the value of the `in_axes` argument to `pmap` "
          "is a tree prefix of the tuple of arguments passed positionally to "
          "the pmapped function."
      )
      raise ValueError(msg) from None

  return in_axes_flat

