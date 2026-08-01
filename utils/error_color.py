
def error_color(
    child: part_interface.RenderableTreePart,
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child in red to indicate errors during rendering."""
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  return ErrorColor(child)

