
def _gather_value_data(game, agent, player):
  """Gathers value data for training."""
  value_buffer = agent.value_buffers[player]
  value_buffer.clear()
  for _ in range(agent.cfg.value_traversals):
    state = game.new_initial_state()
    agent.num_touched += 1
    transitions = []
    while True:
      if state.is_chance_node():
        actions, probs = zip(*state.chance_outcomes())
        a = np.random.choice(actions, p=probs)
        state.apply_action(a)
        continue

      action, importance = -1, 1
      if not state.is_terminal():
        # Get policy.
        obs = np.array(state.information_state_tensor(), dtype=float)
        mask = np.array(state.legal_actions_mask(), dtype=int)
        regret_net = agent.regret_nets[state.current_player()]
        policy = _match_regret(regret_net, obs, mask)

        # Sample action.
        epsilon = agent.cfg.value_exploration
        uniform = mask / np.sum(mask)
        sample_policy = epsilon * uniform + (1 - epsilon) * policy
        action = np.random.choice(range(len(sample_policy)), p=sample_policy)
        importance = policy[action] / sample_policy[action]

      # Add transition.
      history = _state_history(game.num_players(), state)
      returns = np.array(state.returns(), dtype=float)
      tn = Transition(
          history=history, importance=importance, action=action, returns=returns
      )
      transitions.append(tn)

      if state.is_terminal():
        break
      state = state.child(action)
      agent.num_touched += 1

    value = np.zeros(transitions[0].returns.shape, dtype=float)
    for i in range(len(transitions) - 1, -1, -1):
      tn = transitions[i]

      value = tn.importance * (tn.returns + value)
      value_buffer.append(
          StateActionValue(
              state=tn.history, action=tn.action, value=value[player]
          )
      )

