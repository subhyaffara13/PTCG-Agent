
def abbreviation_level(child: RenderableTreePart) -> RenderableTreePart:
  """Marks an abbreviation level, indicating children may be abbreviated."""
  return AbbreviationLevel(child)

