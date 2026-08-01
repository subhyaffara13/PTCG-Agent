
def unbox(tree: Any) -> Any:
  """Strips all AxisMetadata boxes from a PyTree."""
  return map_axis_meta(lambda x: unbox(x.unbox()), tree)

