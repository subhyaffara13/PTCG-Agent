
def custom_text_color(
    child: part_interface.RenderableTreePart, css_color: str
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child that renders in a particular CSS color."""
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  if not isinstance(css_color, str):
    raise ValueError(
        f"`css_color` must be a string, but got {type(css_color).__name__}"
    )
  return CustomTextColor(child, css_color)

