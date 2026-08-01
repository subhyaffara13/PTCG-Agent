
def cfr_br_meta_data(
    history_tree_node: typing.HistoryNode,
    infostate_nodes: List[typing.InfostateNode],
    all_infostates_map: List[typing.InfostateMapping], epochs: int,
    net_apply: typing.ApplyFn, net_params: typing.Params,
    all_actions: List[int], infostate_map: typing.InfostateMapping,
    key: hk.PRNGSequence
) -> tuple[Dict[str, jnp.ndarray], Dict[str, jnp.ndarray], List[float]]:
  """Collects counterfactual values for both players and best response for player_2.

  Args:
    history_tree_node: Game tree HistoryTreeNode which is the root of the game
      tree.
    infostate_nodes: Infostates.
    all_infostates_map: List of mappings from infostate strings to infostates.
    epochs: Number of epochs.
    net_apply: Apply function.
    net_params: Network parameters.
    all_actions: List of all actions.
    infostate_map: A mapping from infostate strings to infostates.
    key: Haiku pseudo random number generator.

  Returns:
    Returns counterfactual values for player_1, counterfactual values for
    player_2 and best response values for player_2.
  """
  counterfactual_values_player1 = {
      infostate.infostate_string: []
      for infostate in list(all_infostates_map[1].values())
  }
  counterfactual_values_player2 = {
      infostate.infostate_string: []
      for infostate in list(all_infostates_map[2].values())
  }

  non_terminal_infostates_map_player1 = utils.filter_terminal_infostates(
      all_infostates_map[1]
  )
  one_hot_representations_player1, illegal_actions_player1 = (
      compute_next_policy_invariants(
          non_terminal_infostates_map_player1, all_actions, infostate_map
      )
  )
  player_2_last_best_response_values = []
  for epoch in range(epochs):
    compute_next_policy(non_terminal_infostates_map_player1, net_apply,
                        net_params, epoch, all_actions,
                        one_hot_representations_player1,
                        illegal_actions_player1, key)

    cfr.compute_reach_probabilities(history_tree_node, all_infostates_map)
    cfr.cumulate_average_policy(list(all_infostates_map[1].values()))
    cfr.compute_best_response_policy(infostate_nodes[2])
    cfr.compute_reach_probabilities(history_tree_node, all_infostates_map)
    cfr.compute_counterfactual_values(infostate_nodes[1])
    cfr.update_regrets(list(all_infostates_map[1].values()))
    append_counterfactual_values(
        list(all_infostates_map[1].values()), counterfactual_values_player1)
    cfr.normalize_average_policy(all_infostates_map[1].values())
    cfr.compute_reach_probabilities(history_tree_node, all_infostates_map)
    player_2_last_best_response_values.append(
        float(cfr.compute_best_response_values(infostate_nodes[2]))
    )

    logging.info(
        "Epoch %d: player_2 best response value is %f",
        epoch,
        player_2_last_best_response_values[-1],
    )

  return (  # pytype: disable=bad-return-type  # jax-ndarray
      counterfactual_values_player1,
      counterfactual_values_player2,
      player_2_last_best_response_values,
  )

