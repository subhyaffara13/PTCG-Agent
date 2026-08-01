
def in_outlined_box(
    child: part_interface.RenderableTreePart,
    css_style: str = "outline: 1px dashed #aaaaaa;",
) -> RenderableTreePart:
  """Wraps a child into an outlined box.

  Outlined boxes ensure that their child appears as a contiguous chunk, instead
  of having its first line indented, so that it can be fully encapsulated in
  a box.

  When rendered to HTML, this class may or may not insert extra newlines before
  and after the child, depending on whether this child was already alone on its
  line. When rendered to text, we always insert extra comments above and below
  the line.

  To allow the box to be collapsed separately, consider wrapping it in a
  foldable node.

  Args:
    child: The child to render.
    css_style: The CSS style for the box element. By default, renders with a
      dashed grey outline.

  Returns:
    A renderable part that renders the child inside a standalone box.
  """
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  if not isinstance(css_style, str):
    raise ValueError(
        f"`css_style` must be a string, but got {type(css_style).__name__}"
    )
  return StyledBoxWithOutline(child, css_style)

