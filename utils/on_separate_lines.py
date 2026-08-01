
def on_separate_lines(
    children: Sequence[RenderableAndLineAnnotations | RenderableTreePart],
) -> RenderableTreePart:
  """Builds a part that renders its children on separate lines.

  The resulting part stacks the children together, moving any comments to the
  end of their lines.

  Args:
    children: Children to render.

  Returns:
    A renderable part that renders the children on separate lines when expanded.
    When collapsed, it instead concatenates them.
  """
  return OnSeparateLines.build(children)

