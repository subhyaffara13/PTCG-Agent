
def robust_child_with_total_reward_tiebreaker(
    root: SearchNode,
) -> tuple[int, SearchNode]:
  """Returns the best action and associated child node.

  The child node with the most visits is chosen.
  In case of a tie, the child with the highest total reward is chosen.


  Args:
    root: The root node of the search tree.

  Returns:
    A tuple containing the best action and the associated child node.
  """
  selection_criteria = lambda node: (node.explore_count, node.total_reward)
  best_child = max(root.children, key=selection_criteria)
  return best_child.action, best_child

