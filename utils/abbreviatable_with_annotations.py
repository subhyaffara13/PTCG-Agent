
def abbreviatable_with_annotations(
    child: part_interface.RenderableAndLineAnnotations,
    abbreviation: RenderableTreePart | None = None,
) -> part_interface.RenderableAndLineAnnotations:
  """Marks an object with annotations as being able to be abbreviated.

  Args:
    object: The object (with annotations) to mark as abbreviatable. This will
        be replaced by the fallback if the object is past the current
        abbreviation depth.
    abbreviation: The fallback to use if the object is abbreviated.
  """
  return part_interface.RenderableAndLineAnnotations(
      HasAbbreviation(child.renderable, abbreviation), child.annotations
  )

