
def expand_to_depth(
    tree: part_interface.RenderableTreePart, depth: int
) -> None:
  """Expands a tree up to a given depth.

  This function ignores the existing expand state, and instead rewrites it to
  expand up to the given depth.

  Args:
    tree: Tree to expand.
    depth: Depth to expand to. At depth 0, all foldables will be collapsed.
  """
  for foldable in tree.foldables_in_this_part():
    if depth > 0:
      foldable.set_expand_state(part_interface.ExpandState.EXPANDED)
      expand_to_depth(foldable.as_expanded_part(), depth - 1)
    else:
      foldable.set_expand_state(part_interface.ExpandState.COLLAPSED)

