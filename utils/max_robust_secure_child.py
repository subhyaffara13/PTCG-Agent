
def max_robust_secure_child(
    root: SearchNode, secure_c: float = 1.0, find_secure: bool = False
) -> tuple[Optional[int], Optional[SearchNode]]:
  """Returns the best action and associated child node.

  A child node with the most visits is chosen.

  Args:
    root: The root node of the search tree.
    secure_c: The constant used to calculate lower uncertainty bound.
    find_secure: Whether to find a secure child node.

  Returns:
    A tuple containing the best action and the associated child node.
  """
  if find_secure:
    best_action, best_child = secure_child(root, secure_c)
  else:
    best_action, best_child = max_robust_child(root)
  return best_action, best_child

