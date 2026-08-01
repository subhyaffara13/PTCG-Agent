
def expand_for_balanced_layout(
    tree: part_interface.RenderableTreePart,
    max_height: int | None = 20,
    target_width: int = 60,
    relax_height_constraint_for_only_child: bool = True,
    recursive_expand_height_for_collapsed_nodes: int = 7,
) -> None:
  """Updates a tree's (weak) expand states to achieve a "balanced" layout.

  A balanced layout tries to evenly allocate space along vertical and horizontal
  axes. Similar to many pretty-printers, nodes are usually expanded to avoid
  long lines and make them fit comfortably within `target_width` characters.
  However, there is also a `max_height` parameter that takes precedence, which
  can be used to prevent outputs from being too large for very large objects,
  and makes it easier for users to interactively expand only the subtrees that
  they want to inspect.

  Unlike other pretty-printers, for simplicity we don't track the current
  indent level or remaining line width, but instead make local decisions for
  each node. This means the overall rendering may end up longer than
  `target_width` because the leaves (each of width `target_width`) may be
  indented. (This simplifies the system because we do not have to track the
  exact indent levels and starting/ending positions of each node, and don't
  have to propagate that information up through the rendered parts.)

  This function only modifies WEAKLY_EXPANDED or WEAKLY_COLLAPSED nodes.

  Args:
    tree: The tree to update.
    max_height: Maximum number of lines for the rendering, which we should try
      not to exceed when expanding nodes. Can sometimes be exceeded for "only
      child" subtrees if `relax_height_constraint_for_only_child` is set. If
      None, then an arbitrary height is allowed, and only `target_width` will be
      used to determine expansion size.
    target_width: Target number of characters for the rendering. If a node is
      shorter than this width when collapsed, we will leave it on a single line
      instead of expanding it.
    relax_height_constraint_for_only_child: If True, we allow the height
      constraint to be violated once if there is only a single node that could
      possibly be expanded. In particular, we repeatedly expand nodes until we
      reach a node shorter than `target_width` or a node with two or more
      children. If we match or exceed the height constraint while doing this, we
      stop after expanding that node (but leave it expanded). If we haven't
      reached the constraint, we continue expanding under the stricter rules.
    recursive_expand_height_for_collapsed_nodes: Whenever we mark a node as
      collapsed, we first recursively expand its children as if it was expanded
      with this as the max height, then collapse only the outermost node. This
      means it will render as a single line, but if expanded by the user, it
      will expand not just the clicked node but also some of its children. This
      is intended to support faster interactive exploration of large objects.
  """
  # Tracks the number of lines we have so far committed to outputting via our
  # expansion decisions.
  committed_height = 1 + tree.newlines_in_expanded_parent
  # Tracks the collection of foldable nodes we can consider expanding.
  candidate_foldables = collections.deque(tree.foldables_in_this_part())

  # Step 1: Handle only children.
  if relax_height_constraint_for_only_child:
    while (
        # We haven't yet reached the height constraint.
        (max_height is None or committed_height < max_height)
        # There's only one node that could be expanded.
        and len(candidate_foldables) == 1
        # This node doesn't fit in the target width.
        and candidate_foldables[0].collapsed_width > target_width
        # This node isn't already forced to be collapsed.
        and candidate_foldables[0].get_expand_state()
        != part_interface.ExpandState.COLLAPSED
    ):
      # We should expand this node.
      foldable = candidate_foldables.popleft()
      expanded_foldable_contents = foldable.as_expanded_part()
      foldable.set_expand_state(part_interface.ExpandState.EXPANDED)
      committed_height += expanded_foldable_contents.newlines_in_expanded_parent
      candidate_foldables.extend(
          expanded_foldable_contents.foldables_in_this_part()
      )

  # Step 2: Expand nodes in breadth-first order while we have space.
  while candidate_foldables:
    foldable = candidate_foldables.popleft()
    expanded_foldable_contents = foldable.as_expanded_part()

    if foldable.get_expand_state().is_weak():
      # Infer a state for this node.
      height_if_expanded = (
          committed_height
          + expanded_foldable_contents.newlines_in_expanded_parent
      )
      if max_height is not None and height_if_expanded > max_height:
        # This node takes up too much space if expanded. Collapse it.
        foldable.set_expand_state(part_interface.ExpandState.COLLAPSED)
      elif foldable.collapsed_width > target_width:
        # This node is too long to render on one line. Expand it.
        foldable.set_expand_state(part_interface.ExpandState.EXPANDED)
      else:
        # This node could render either collapsed or expanded. Commit to its
        # current weak preference.
        if (
            foldable.get_expand_state()
            == part_interface.ExpandState.WEAKLY_EXPANDED
        ):
          foldable.set_expand_state(part_interface.ExpandState.EXPANDED)
        else:
          foldable.set_expand_state(part_interface.ExpandState.COLLAPSED)

    if foldable.get_expand_state() == part_interface.ExpandState.EXPANDED:
      # Record it as expanded and add children to our queue.
      committed_height += expanded_foldable_contents.newlines_in_expanded_parent
      candidate_foldables.extend(
          expanded_foldable_contents.foldables_in_this_part()
      )
    else:
      # Recursively process the children with this function, and don't add them
      # to the current queue (since their parent isn't expanded)
      expand_for_balanced_layout(
          expanded_foldable_contents,
          max_height=recursive_expand_height_for_collapsed_nodes,
          target_width=target_width,
          relax_height_constraint_for_only_child=(
              relax_height_constraint_for_only_child
          ),
          recursive_expand_height_for_collapsed_nodes=(
              recursive_expand_height_for_collapsed_nodes
          ),
      )

