
def _process_foldable_by_marks(
    foldable: part_interface.FoldableTreeNode,
    marks: Collection[Any],
    collapse_weak_others: bool,
) -> bool:
  """Expands a foldable based on marks, and may also collapse its children.

  Args:
    foldable: The foldable to process.
    marks: The marks that should be made visible.
    collapse_weak_others: Whether to collapse foldables that do NOT have the
      given marks and have a weak expansion state.

  Returns:
    True if this node should be made visible (e.g. all parents expanded) based
    on the marks.
  """
  # Check children.
  might_need_collapsing = []
  for child_foldable in foldable.as_expanded_part().foldables_in_this_part():
    if not _process_foldable_by_marks(
        child_foldable, marks, collapse_weak_others
    ):
      might_need_collapsing.append(child_foldable)

  if any(mark in foldable.layout_marks_in_this_part for mark in marks):
    # We need to expand this node.
    foldable.set_expand_state(part_interface.ExpandState.EXPANDED)
    if collapse_weak_others:
      # We should also collapse any child that wasn't marked as needing to be
      # expanded.
      for child_foldable in might_need_collapsing:
        if child_foldable.get_expand_state().is_weak():
          child_foldable.set_expand_state(part_interface.ExpandState.COLLAPSED)
    # Inform caller that we found something.
    return True
  else:
    # This node doesn't need to be expanded. Don't immediately mark it as
    # collapsed, because we may want to mark a parent as collapsed instead.
    # The parent will collapse this node if necessary.
    return False

