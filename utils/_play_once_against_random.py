
def _play_once_against_random(game, agent):
  """Plays one game against a random policy and returns the reward."""
  reward = 0
  for player in range(game.num_players()):
    state = game.new_initial_state()
    while not state.is_terminal():
      if state.is_chance_node():
        outcomes, probs = zip(*state.chance_outcomes())
        a = np.random.choice(outcomes, p=probs)
        state.apply_action(a)
        continue

      if state.current_player() == player:
        policy = agent.action_probabilities(state)
      else:
        mask = np.array(state.legal_actions_mask(), dtype=int)
        policy = mask / np.sum(mask)
      action = np.random.choice(range(len(policy)), p=policy)
      state.apply_action(action)

    reward += state.returns()[player]

  return reward / game.num_players()

