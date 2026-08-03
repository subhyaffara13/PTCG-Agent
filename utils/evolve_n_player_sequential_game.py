import random

def evolve_n_player_sequential_game(seq_game, policy, graph, debug=False):
  state = seq_game.new_initial_state()
  while not state.is_terminal():
    legal_actions = state.legal_actions()
    if state.is_chance_node():
      # Sample a chance event outcome.
      outcomes_with_probs = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes_with_probs)
      action = np.random.choice(action_list, p=prob_list)
      if debug:
        print("------------ Change node ------------")
        print(
            (f"Possible chance actions: {outcomes_with_probs}, the one taken: "
             f"{action}."))
      state.apply_action(action)
    else:
      if debug:
        print("------------ Sequential action node ------------")
        print(state.information_state_tensor())
        print(state.observation_tensor())
        print(state.information_state_string())
      if policy is not None:
        state_policy = policy(state)
        vehicle_location = [
            s.replace("'", "")
            for s in str(state).split("[")[1].split("]")[0].split(", ")
        ]
        if debug:
          print((f"Policy for player {state.current_player()} at location "
                 f"{vehicle_location[state.current_player()]}: ") +
                str([(str(graph.get_road_section_from_action_id(k)) +
                      f"with probability {v}")
                     for k, v in state_policy.items()]))
        assert set(state_policy) == set(legal_actions)
        action = random.choices(legal_actions,
                                [state_policy[a] for a in legal_actions])
        assert len(action) == 1
        action = action[0]
      else:
        action = random.choice(legal_actions)
      state.apply_action(action)
      vehicle_location = [
          s.replace("'", "")
          for s in str(state).split("[")[1].split("]")[0].split(", ")
      ]
      if debug:
        print(vehicle_location)
      plot_network_n_player_game(
          graph,
          [graph.return_position_of_road_section(x) for x in vehicle_location])
  if debug:
    print(f"Travel times: {[-x for x in state.returns()]}")

