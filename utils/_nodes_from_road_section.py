
def _nodes_from_road_section(movement: str) -> tuple[str, str]:
  """Split a road section 'A->B' to two nodes 'A' and 'B'."""
  origin, destination = movement.split("->")
  return origin, destination

