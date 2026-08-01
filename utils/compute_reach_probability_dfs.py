
def compute_reach_probability_dfs(
    history_tree_node: HistoryNode,
    all_infostates_map: List[InfostateMapping]) -> None:
  """Calculate reach probability values in dfs tree.

  This function is initially called by compute_reach_probabilities and it
  computes reach probabilities for all information state nodes in the tree by
  traversing the tree using DFS.

  Args:
    history_tree_node: Game tree HistoryTreeNode which is the root of the game
      tree.
    all_infostates_map: List of dictionaries (mapping from information state
      string representation to information state object) for each players
      (including chance player). This list will be empty when this function is
      called fot the first time and it'll be population during DFS tree
      traversal.
  """

  world_state = history_tree_node.world_state
  infostate_p1 = all_infostates_map[Players.PLAYER_1][
      world_state.get_infostate_string(Players.PLAYER_1)]
  infostate_p2 = all_infostates_map[Players.PLAYER_2][
      world_state.get_infostate_string(Players.PLAYER_2)]
  infostate_p1.counterfactual_reach_prob += history_tree_node.reach_probs[
      0] * history_tree_node.reach_probs[Players.PLAYER_2]
  infostate_p2.counterfactual_reach_prob += history_tree_node.reach_probs[
      0] * history_tree_node.reach_probs[Players.PLAYER_1]

  if infostate_p1.player_reach_prob != 0.:
    assert (infostate_p1.player_reach_prob == history_tree_node.reach_probs[
        Players.PLAYER_1])

  if infostate_p2.player_reach_prob != 0.:
    assert (infostate_p2.player_reach_prob == history_tree_node.reach_probs[
        Players.PLAYER_2])

  infostate_p1.player_reach_prob = history_tree_node.reach_probs[
      Players.PLAYER_1]
  infostate_p2.player_reach_prob = history_tree_node.reach_probs[
      Players.PLAYER_2]

  policy_p1 = infostate_p1.policy
  policy_p2 = infostate_p2.policy
  policy_chance = world_state.chance_policy
  actions_chance, actions_p1, actions_p2 = world_state.get_actions()
  for action_chance in actions_chance:
    for action_p1 in actions_p1:
      for action_p2 in actions_p2:
        history_tree_node.action_probs[(
            action_chance, action_p1, action_p2)] = policy_chance[
                action_chance] * policy_p1[action_p1] * policy_p2[action_p2]
        child_node = history_tree_node.get_child(
            (action_chance, action_p1, action_p2))
        child_node.reach_probs[
            Players.CHANCE_PLAYER] = history_tree_node.reach_probs[
                Players.CHANCE_PLAYER] * policy_chance[action_chance]
        child_node.reach_probs[
            Players.PLAYER_1] = history_tree_node.reach_probs[
                Players.PLAYER_1] * policy_p1[action_p1]
        child_node.reach_probs[
            Players.PLAYER_2] = history_tree_node.reach_probs[
                Players.PLAYER_2] * policy_p2[action_p2]
        compute_reach_probability_dfs(child_node, all_infostates_map)

