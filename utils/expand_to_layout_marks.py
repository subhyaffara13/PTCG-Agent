
def expand_to_layout_marks(
    tree: part_interface.RenderableTreePart,
    marks: Collection[Any],
    collapse_weak_others: bool,
) -> None:
  """Expands a tree so that any part with a marker in the given set is visible.

  This function ignores the existing expand state, and instead just ensures that
  every foldable node that contains a layout marker in `marks` is expanded.
  Optionally it will also ensure that all sibling foldable nodes are collapsed.

  Expand states for those nodes are set to EXPANDED or COLLAPSED, and expand
  states for other nodes are not modified. This means you can call
  `expand_for_balanced_layout` after this function to reformat the subtrees
  of `tree` that haven't yet been assigned strong expand/collapse states. This
  is useful for producing balanced layouts once the user expands a collapsed
  node.

  Args:
    tree: The tree to update.
    marks: The marks that should be made visible.
    collapse_weak_others: Whether to collapse foldables that do NOT have the
      given marks and have a weak expansion state.
  """
  for foldable in tree.foldables_in_this_part():
    found = _process_foldable_by_marks(foldable, marks, collapse_weak_others)
    if collapse_weak_others and not found:
      foldable.set_expand_state(part_interface.ExpandState.COLLAPSED)

