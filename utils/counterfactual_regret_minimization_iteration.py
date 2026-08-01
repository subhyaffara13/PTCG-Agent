
def counterfactual_regret_minimization_iteration(
    cfr_game_tree: GameTree,
    alternating_updates: bool,
    cfr_plus: bool,
    weight: int = 1) -> None:
  """Performs one iteration of CFR or CFR-plus.

  Args:
    cfr_game_tree: Game tree for an imperfect information game. This game tree
      is game tree of an openspiel game.
    alternating_updates: Boolean flag to do alternative update for players
      policies or not. If True, alternative updates will be performed (meaning
      we first calculate average policy, counterfactual values, regrets and next
      policy for player 1 first and then calculate all of these for player 2),
      otherwise both players average policies, counterfactual values and regrets
      will be updated right after each other (meaning, for example we calculate
      next_policy of player 1, and then next policy of player 2. Then, we
      calculate average policy for player 1 and then average policy for player
      2, and so on).
    cfr_plus: Boolean flag indicating if we perform CFR algorithm or CFR-plus.
      If True, we perform CFR-plus algorithm, otherwise we perform CFR
      algorithm.
    weight: The weight we use to update policy and sum of weighted average
      policy.
  """
  if alternating_updates:
    compute_reach_probabilities(cfr_game_tree.first_history_node,
                                cfr_game_tree.all_infostates_map)
    cumulate_average_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()),
        weight)
    compute_counterfactual_values(
        cfr_game_tree.infostate_nodes[Players.PLAYER_1])
    update_regrets(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()))
    compute_next_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()),
        cfr_plus)

    compute_reach_probabilities(cfr_game_tree.first_history_node,
                                cfr_game_tree.all_infostates_map)
    cumulate_average_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()),
        weight)
    compute_counterfactual_values(
        cfr_game_tree.infostate_nodes[Players.PLAYER_2])
    update_regrets(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()))
    compute_next_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()),
        cfr_plus)
  else:
    compute_next_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()),
        cfr_plus)
    compute_next_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()),
        cfr_plus)

    compute_reach_probabilities(cfr_game_tree.first_history_node,
                                cfr_game_tree.all_infostates_map)
    cumulate_average_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()),
        weight)
    cumulate_average_policy(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()),
        weight)

    compute_counterfactual_values(
        cfr_game_tree.infostate_nodes[Players.PLAYER_1])
    compute_counterfactual_values(
        cfr_game_tree.infostate_nodes[Players.PLAYER_2])

    update_regrets(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_1].values()))
    update_regrets(
        list(cfr_game_tree.all_infostates_map[Players.PLAYER_2].values()))

