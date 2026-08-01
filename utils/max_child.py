
def max_child(root: SearchNode) -> tuple[int, SearchNode]:
  """Returns the best action and associated child node.

  A child node with the highest expected reward is chosen.

  Args:
    root: The root node of the search tree.

  Returns:
    A tuple containing the best action and the associated child node.
  """
  selection_criteria = (
      lambda node: node.total_reward / node.explore_count
      if node.explore_count
      else float("-inf")
  )
  best_child = max(root.children, key=selection_criteria)
  return best_child.action, best_child

