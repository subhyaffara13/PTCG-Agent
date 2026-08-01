
def build_full_line_with_annotations(
    *args: str | RenderableTreePart | RenderableAndLineAnnotations,
) -> RenderableTreePart:
  """Concatenates tree parts and appends their line comments at the end.

  To ensure that the output is formatted correctly, the output of this function
  should always appear at the end of a line when its parent is expanded. This
  is not checked. (Failing to do this may cause delimiters to be erroneously
  commented out.)

  Args:
    *args: Sequence of strings, renderable tree parts, or commented tree parts
      to render.

  Returns:
    A renderable tree part that combines all of the main renderables, and also
    shows the line annotations on the right when expanded.
  """
  combined = siblings_with_annotations(*args)
  if (
      combined.annotations is None
      or isinstance(combined.annotations, EmptyPart)
      or (
          isinstance(combined.annotations, Siblings)
          and not combined.annotations.children
      )
  ):
    return combined.renderable
  return siblings(
      combined.renderable,
      FoldCondition(expanded=combined.annotations),
  )

