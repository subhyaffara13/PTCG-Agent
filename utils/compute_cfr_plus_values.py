
def compute_cfr_plus_values(cfr_game_tree: GameTree,
                            steps: int) -> Tuple[List[float], List[float]]:
  """Performs CFR-plus algorithm for a given number of steps.

  Args:
    cfr_game_tree: Game tree for an imperfect information game. This game tree
      is game tree of an openspiel game.
    steps: Number of CFR-plus steps.

  Returns:
    best_response_values_p1: List of best response values for player 1. The
    length of this list is equal to the number of steps.
    best_response_values_p2: List of best response values for player 2. The
    length of this list is equal to the number of steps.
  """
  best_response_values_p1 = []
  best_response_values_p2 = []
  for i in range(steps):
    counterfactual_regret_minimization_iteration(
        cfr_game_tree=cfr_game_tree,
        alternating_updates=True,
        cfr_plus=True,
        weight=i + 1)

    game_tree_copy = copy.deepcopy(cfr_game_tree)
    normalize_average_policy(
        game_tree_copy.all_infostates_map[Players.PLAYER_1].values())
    normalize_average_policy(
        game_tree_copy.all_infostates_map[Players.PLAYER_2].values())
    compute_reach_probabilities(game_tree_copy.first_history_node,
                                game_tree_copy.all_infostates_map)

    best_response_values_p1.append(
        compute_best_response_values(
            game_tree_copy.infostate_nodes[Players.PLAYER_1]))
    best_response_values_p2.append(
        compute_best_response_values(
            game_tree_copy.infostate_nodes[Players.PLAYER_2]))

  return best_response_values_p1, best_response_values_p2

