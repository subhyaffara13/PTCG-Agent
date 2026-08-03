from typing import Optional

def max_robust_child(
    root: SearchNode, find_robust: bool = False
) -> tuple[Optional[int], Optional[SearchNode]]:
  """Returns the best action and associated child node.

  A child node with the highest expected reward and most visits is chosen.
  If no such child exists, increase the number of simulations.

  Args:
    root: The root node of the search tree.
    find_robust: Whether to find a robust child node. E.g., if max compute is
      reached and max robust is not found.

  Returns:
    A tuple containing the best action and the associated child node.
  """
  if find_robust:
    best_action, best_child = robust_child(root)
  else:
    _, max_child_node = max_child(root)
    _, robust_child_node = robust_child(root)
    best_action, best_child = None, None
    for child in root.children:
      if child == max_child_node and child == robust_child_node:
        best_action, best_child = child.action, child
        break
  return best_action, best_child

