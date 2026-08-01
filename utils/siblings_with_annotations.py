
def siblings_with_annotations(
    *args: str | RenderableTreePart | RenderableAndLineAnnotations,
    extra_annotations: Sequence[RenderableTreePart] = (),
) -> RenderableAndLineAnnotations:
  """Combines siblings that may have annotations, aggregating separately.

  This can be used to lay out multiple objects on the same line, when some
  may have annotations.

  Args:
    *args: Sequence of strings, renderable tree parts, or commented tree parts
      to render.
    extra_annotations: Additional annotations to add.

  Returns:
    A new pair of renderable and annotations, with main renderables and
    annotations combined separately.
  """
  parts = []
  annotations = []
  for arg in args:
    if isinstance(arg, RenderableTreePart):
      parts.append(arg)
    elif isinstance(arg, str):
      parts.append(Text(arg))
    elif isinstance(arg, RenderableAndLineAnnotations):
      parts.append(arg.renderable)
      if arg.annotations is not None:
        annotations.append(arg.annotations)
    else:
      raise ValueError(
          "Expected a renderable tree part (possibly with line annotations) or"
          f" a string, but got: {type(arg)}"
      )

  for annotation in extra_annotations:
    annotations.append(annotation)

  return RenderableAndLineAnnotations(siblings(*parts), siblings(*annotations))

