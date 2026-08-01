
def sample_episode(state, policies):
  """Samples an episode using policies, starting from state.

  Args:
    state: Pyspiel state representing the current state.
    policies: List of policy representing the policy executed by each player.

  Returns:
    The result of the call to returns() of the final state in the episode.
        Meant to be a win/loss integer.
  """
  if state.is_terminal():
    return np.array(state.returns(), dtype=np.float32)

  if state.is_simultaneous_node():
    actions = [None] * state.num_players()
    for player in range(state.num_players()):
      state_policy = policies[player](state, player)
      outcomes, probs = zip(*state_policy.items())
      actions[player] = utils.random_choice(outcomes, probs)
    state.apply_actions(actions)
    return sample_episode(state, policies)

  if state.is_chance_node():
    outcomes, probs = zip(*state.chance_outcomes())
  else:
    player = state.current_player()
    state_policy = policies[player](state)
    outcomes, probs = zip(*state_policy.items())

  state.apply_action(utils.random_choice(outcomes, probs))
  return sample_episode(state, policies)

