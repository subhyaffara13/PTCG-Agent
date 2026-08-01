
def build_custom_foldable_tree_node(
    contents: RenderableTreePart,
    path: str | None = None,
    label: RenderableTreePart = basic_parts.EmptyPart(),
    expand_state: part_interface.ExpandState = (
        part_interface.ExpandState.WEAKLY_COLLAPSED
    ),
) -> RenderableAndLineAnnotations:
  """Builds a custom foldable tree node with path buttons.

  Args:
    contents: Contents of this foldable that should not open/close the custom
      foldable when clicked.
    path: Keypath to this node from the root. If provided, a copy-path button
      will be added at the end of the node.
    label: The beginning of the first line, which should allow opening/closing
      the custom foldable when clicked. Should not contain any other foldables.
    expand_state: Initial expand state for the foldable.

  Returns:
    A new renderable part, possibly with a copy button annotation, for use
    in part of a rendered treescope tree.
  """
  maybe_copy_button = build_copy_button(path)

  return RenderableAndLineAnnotations(
      renderable=foldable_impl.FoldableTreeNodeImpl(
          label=label, contents=contents, expand_state=expand_state
      ),
      annotations=maybe_copy_button,
  )

