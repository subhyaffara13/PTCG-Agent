
def with_layout_mark(
    child: RenderableTreePart, mark: Hashable
) -> RenderableTreePart:
  """Returns a part that marks its child for layout purposes.

  Args:
    child: Contents of the group.
    mark: A layout mark to apply to the child. This can later be used by layout
      algorithms to show this node.

  Returns:
    A new part that marks its child for layout purposes.
  """
  if not isinstance(child, RenderableTreePart):
    raise ValueError(f"child must be a renderable part, got {type(child)}")
  if not isinstance(mark, Hashable):
    raise ValueError(f"Layout marks must be hashable, got {mark}")
  return WithLayoutMark(child=child, mark=mark)

