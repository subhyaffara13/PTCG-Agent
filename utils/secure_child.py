import math


def secure_child(
    root: SearchNode, secure_c: float = 1.0
) -> tuple[int, SearchNode]:
  """Returns the best action and associated child node.

  A child node with the most visits is chosen.

  Args:
    root: The root node of the search tree.
    secure_c: The constant used to calculate lower uncertainty bound

  Returns:
    A tuple containing the best action and the associated child node.
  """
  selection_criteria = (
      lambda node: node.total_reward / node.explore_count  # pylint: disable=g-long-ternary
      - secure_c / math.sqrt(node.explore_count)
      if node.explore_count
      else float("-inf")
  )
  best_child = max(root.children, key=selection_criteria)
  return best_child.action, best_child

