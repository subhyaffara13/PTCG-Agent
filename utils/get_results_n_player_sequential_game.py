
def get_results_n_player_sequential_game(seq_game, policy):
  state = seq_game.new_initial_state()
  while not state.is_terminal():
    legal_actions = state.legal_actions()
    if state.is_chance_node():
      outcomes_with_probs = state.chance_outcomes()
      action_list, prob_list = zip(*outcomes_with_probs)
      action = np.random.choice(action_list, p=prob_list)
    else:
      state_policy = policy(state)
      assert set(state_policy) == set(legal_actions)
      action = random.choices(legal_actions,
                              [state_policy[a] for a in legal_actions])
      assert len(action) == 1
      action = action[0]
    state.apply_action(action)
  return state.returns()

