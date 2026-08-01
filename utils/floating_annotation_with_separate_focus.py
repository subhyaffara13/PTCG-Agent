
def floating_annotation_with_separate_focus(
    child: part_interface.RenderableTreePart,
) -> part_interface.RenderableTreePart:
  """Wraps a child so that selections outside it don't include it.

  It is sometimes useful to add additional annotations to an object that aren't
  pretty-printed parts of that object. This causes some problems for ordinary
  roundtrip mode, since we want it to be possible to exactly round-trip an
  object based on its printed representation.

  This object marks its child so that it doesn't get selected by the mouse
  when the selection starts outside the node. This means that if you copy the
  object normally, you don't copy the annotation, so that what you copied
  stays roundtrippable.

  In text mode, selections can't be manipulated. We fake the same thing by
  rendering it as a "comment" (by adding comment markers before every line)
  and hiding it if collapsed.

  Args:
    child: Child to render.

  Returns:
    A wrapped version of ``child`` that does not participate in text selection
    in HTML mode, and adds comments in text mode.
  """
  if not isinstance(child, RenderableTreePart):
    raise ValueError(
        f"`child` must be a renderable part, but got {type(child).__name__}"
    )
  return ScopedSelectableAnnotation(child)

