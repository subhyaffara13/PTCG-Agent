
def indented_children(
    children: Sequence[RenderableAndLineAnnotations | RenderableTreePart],
    comma_separated: bool = False,
    force_trailing_comma: bool = False,
) -> RenderableTreePart:
  """Builds a IndentedChildren instance, supporting annotations and delimiters.

  This method stacks the children together, optionally inserting delimiters,
  and moving any comments to the end of their lines.

  Args:
    children: Children to render.
    comma_separated: Whether to automatically insert commas between children. If
      False, delimiters can be manually inserted into `children` first instead.
    force_trailing_comma: Whether to render a trailing comma in collapsed mode.

  Returns:
    A renderable part that renders the children on separate lines with an
    indent. When collapsed, it instead concatenates them.
  """
  return IndentedChildren.build(
      children=children,
      comma_separated=comma_separated,
      force_trailing_comma=force_trailing_comma,
  )

