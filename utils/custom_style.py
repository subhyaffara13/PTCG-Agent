
def custom_style(
    child: part_interface.RenderableTreePart,
    css_style: str,
) -> part_interface.RenderableTreePart:
  """Returns a wrapped child with a custom CSS style.

  Args:
    child: Child to render.
    css_style: A CSS style string.

  Returns:
    A wrapped child with a custom CSS style applied. Intended for an inline
    text component.
  """
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  if not isinstance(css_style, str):
    raise ValueError(
        f"`css_style` must be a string, but got {type(css_style).__name__}"
    )
  return CSSStyled(child, css_style)

