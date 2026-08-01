
def comment_color(
    child: part_interface.RenderableTreePart,
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child in a color for comments."""
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  return CommentColor(child)

