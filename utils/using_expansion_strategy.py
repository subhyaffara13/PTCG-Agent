import functools

def using_expansion_strategy(
    max_height: int | None = 20,
    target_width: int = 60,
    relax_for_only_child: bool = True,
    recursive_expand_height: int = 7,
) -> contextlib.AbstractContextManager[None]:
  """Context manager that modifies the expansion strategy of Treescope.

  This is a convenience function for modifying the layout algorithm used by
  Treescope to determine how many nodes to expand by default. It returns a
  context manager within which the given balanced expansion strategy will be
  used.

  Args:
    max_height: Maximum number of lines for the rendering, which we should try
      not to exceed when expanding nodes. Can sometimes be exceeded for "only
      child" subtrees if ``relax_for_only_child`` is set. If None, then an
      arbitrary height is allowed, and only ``target_width`` will be used to
      determine expansion size.
    target_width: Target number of characters for the rendering. If a node is
      shorter than this width when collapsed, we will leave it on a single line
      instead of expanding it.
    relax_for_only_child: If True, we allow the height constraint to be violated
      once if there is only a single node that could possibly be expanded. In
      particular, we repeatedly expand nodes until we reach a node shorter than
      ``target_width`` or a node with two or more children. If we match or
      exceed the height constraint while doing this, we stop after expanding
      that node (but leave it expanded). If we haven't reached the constraint,
      we continue expanding under the stricter rules.
    recursive_expand_height: Whenever we mark a node as collapsed, we first
      recursively expand its children as if it was expanded with this as the max
      height, then collapse only the outermost node. This means it will render
      as a single line, but if expanded by the user, it will expand not just the
      clicked node but also some of its children. This is intended to support
      faster interactive exploration of large objects.

  Returns:
    Context manager in which the given strategy will be active.
  """
  return active_expansion_strategy.set_scoped(
      functools.partial(
          layout_algorithms.expand_for_balanced_layout,
          max_height=max_height,
          target_width=target_width,
          relax_height_constraint_for_only_child=relax_for_only_child,
          recursive_expand_height_for_collapsed_nodes=recursive_expand_height,
      )
  )

