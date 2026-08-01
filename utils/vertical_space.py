
def vertical_space(css_height: str) -> RenderableTreePart:
  """Returns a vertical space with the given height in HTML mode.

  Args:
    css_height: The height of the space, as a CSS length string.

  Returns:
    A renderable part that renders as a vertical space in HTML mode, and does
    not render in text mode.
  """
  if not isinstance(css_height, str):
    raise ValueError(f"css_height must be a string, got {css_height}")
  return VerticalSpace(height=css_height)

