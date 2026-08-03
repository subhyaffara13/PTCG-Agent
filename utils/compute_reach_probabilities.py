from typing import List

def compute_reach_probabilities(
    history_tree_node: HistoryNode,
    all_infostates_map: List[InfostateMapping]) -> None:
  """Computes reach probabilities for game tree information states.

  This function initializes counterfactual_reach_prob and player_reach_prob for
  all information states in the game tree, and then these values will be
  calculated in compute_reach_probability_dfs.

  Args:
    history_tree_node: Game tree HistoryTreeNode which is the root of the game
      tree.
    all_infostates_map: List of dictionaries (mapping from information state
      string representation to information state object) for each players
      (including chance player). This list will be empty when this function is
      called fot the first time and it'll be population during DFS tree
      traversal.
  """

  for infostate in (list(all_infostates_map[Players.PLAYER_1].values()) +
                    list(all_infostates_map[Players.PLAYER_2].values())):
    infostate.counterfactual_reach_prob = 0.
    infostate.player_reach_prob = 0.
  compute_reach_probability_dfs(history_tree_node, all_infostates_map)

