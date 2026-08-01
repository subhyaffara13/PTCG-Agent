
def abbreviatable(
    child: RenderableTreePart, abbreviation: RenderableTreePart | None = None
) -> RenderableTreePart:
  """Marks an object as being able to be abbreviated.

  Args:
    object: The object to mark as abbreviatable. This will be replaced by the
        fallback if the object is past the current abbreviation depth.
    abbreviation: The fallback to use if the object is abbreviated.
  """
  if abbreviation is None:
    abbreviation = basic_parts.siblings(
        common_styles.comment_color(basic_parts.text("<")),
        common_styles.abbreviation_color(basic_parts.text("...")),
        common_styles.comment_color(basic_parts.text(">")),
    )
  return HasAbbreviation(child, abbreviation)

