
def evolve_n_player_simultaneous_game(game, policy, graph):
  state = game.new_initial_state()
  i = 0
  while not state.is_terminal():
    i += 1
    if state.is_chance_node():
      # Sample a chance event outcome.
      outcomes_with_probs = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes_with_probs)
      action = np.random.choice(action_list, p=prob_list)
      state.apply_action(action)
    elif state.is_simultaneous_node():
      # Simultaneous node: sample actions for all players.
      chosen_actions = []
      for i in range(game.num_players()):
        legal_actions = state.legal_actions(i)
        state_policy = policy(state, i)
        assert len(legal_actions) == len(state_policy), (
            f"{legal_actions} not same length than {state_policy}")
        chosen_actions.append(
            random.choices(legal_actions,
                           [state_policy[a] for a in legal_actions])[0])
      state.apply_actions(chosen_actions)
    else:
      raise ValueError(
          "State should either be simultaneous node or change node.")
    plot_network_n_player_game(graph, [
        graph.return_position_of_road_section(x)
        for x in state.get_current_vehicle_locations()
    ])
  print(f"Travel times: {[-x for x in state.returns()]}")

