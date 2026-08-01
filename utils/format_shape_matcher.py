
def format_shape_matcher(shape: TShapeMatcher) -> str:
  return f"({', '.join('...' if d is Ellipsis else str(d) for d in shape)})"  # pylint: disable=inconsistent-quotes

