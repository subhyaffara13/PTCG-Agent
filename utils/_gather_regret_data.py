
def _gather_regret_data(game, agent, player):
  """Gathers regret data for training."""
  for _ in range(agent.cfg.regret_traversals):
    state = game.new_initial_state()
    agent.num_touched += 1
    while not state.is_terminal():
      if state.is_chance_node():
        actions, probs = zip(*state.chance_outcomes())
        a = np.random.choice(actions, p=probs)
        state.apply_action(a)
        continue

      # Get policy.
      current_player = state.current_player()
      obs = np.array(state.information_state_tensor(), dtype=float)
      mask = np.array(state.legal_actions_mask(), dtype=int)
      policy = _match_regret(agent.regret_nets[current_player], obs, mask)

      # Add data to buffer.
      if current_player == player:
        regret = _get_regret(agent, state, policy, game.num_players())
        sr = StateRegret(state=obs, regret=regret, mask=mask, t=agent.t)
        agent.regret_buffers[player].append(sr)
      else:
        behaviour = Behaviour(state=obs, policy=policy, t=agent.t)
        agent.avg_policy_buffer.append(behaviour)

      # Update state with policy.
      if current_player == player:
        sample_policy = mask / np.sum(mask)
      else:
        sample_policy = policy
      action = np.random.choice(range(len(sample_policy)), p=sample_policy)
      state = state.child(action)
      agent.num_touched += 1

