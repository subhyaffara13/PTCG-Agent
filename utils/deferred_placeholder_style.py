
def deferred_placeholder_style(
    child: part_interface.RenderableTreePart,
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child in italics to indicate a deferred placeholder."""
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  return DeferredPlaceholderStyle(child)

