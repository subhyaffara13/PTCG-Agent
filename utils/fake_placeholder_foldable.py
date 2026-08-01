
def fake_placeholder_foldable(
    placeholder_content: RenderableTreePart, extra_newlines_guess: int
) -> FoldableTreeNode:
  """Builds a fake placeholder for deferred renderings.

  The main use for this is is to return as the placeholder for a deferred
  rendering, so that it can participate in layout decisions. The
  `get_expand_state` method can be used to infer whether the part was
  collapsed while deferred.

  Args:
    placeholder_content: The content of the placeholder to render.
    extra_newlines_guess: The number of fake newlines to pretend this object
      has.

  Returns:
    A foldable node that does not have any actual content, but pretends to
    contain the given number of newlines for layout decisions.
  """
  return FoldableTreeNodeImpl(
      contents=basic_parts.siblings(
          placeholder_content,
          EmptyWithHeightGuess(fake_newlines=extra_newlines_guess),
      ),
      expand_state=ExpandState.WEAKLY_EXPANDED,
  )

