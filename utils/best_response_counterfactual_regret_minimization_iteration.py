
def best_response_counterfactual_regret_minimization_iteration(
    history_tree_node: HistoryNode,
    infostate_nodes: List[InfostateNode],
    all_infostates_map: List[InfostateMapping]) -> None:
  """Calculates CFRBR values.

  Args:
    history_tree_node: Game tree HistoryTreeNode which is the root of the game
      tree.
    infostate_nodes: List of all information state nodes.
    all_infostates_map: List of dictionaries (mapping from information state
      string representation to information state object) for each players
      (including chance player). This list will be empty when this function is
      called fot the first time and it'll be population during DFS tree
      traversal.
  """
  compute_next_policy(list(all_infostates_map[Players.PLAYER_1].values()))

  compute_reach_probabilities(history_tree_node, all_infostates_map)
  cumulate_average_policy(list(all_infostates_map[Players.PLAYER_1].values()))

  compute_best_response_policy(infostate_nodes[Players.PLAYER_2])
  compute_reach_probabilities(history_tree_node, all_infostates_map)
  compute_counterfactual_values(infostate_nodes[Players.PLAYER_1])

  update_regrets(list(all_infostates_map[Players.PLAYER_1].values()))

