
def sample_value(
    pi: policy_std.Policy, mu: distribution_std.Distribution, game
):
  """Samples the value of playing `pi` against distribution `mu`.

  Args:
    pi: A policy object whose value is evaluated against `mu`.
    mu: A distribution object against which `pi` is evaluated.
    game: A pyspiel.Game object, the evaluation game.

  Returns:
    Sampled value of `pi` in `game` against `mu`.
  """
  mfg_state = game.new_initial_states()[0]
  total_reward = 0.0
  while not mfg_state.is_terminal():
    if mfg_state.current_player() == pyspiel.PlayerId.CHANCE:
      action_list, prob_list = zip(*mfg_state.chance_outcomes())
      action = np.random.choice(action_list, p=prob_list)
      mfg_state.apply_action(action)
    elif mfg_state.current_player() == pyspiel.PlayerId.MEAN_FIELD:
      dist_to_register = mfg_state.distribution_support()
      dist = [mu.value_str(str_state, 0.0) for str_state in dist_to_register]
      mfg_state.update_distribution(dist)
    else:
      total_reward += mfg_state.rewards()[0]
      action_prob = pi(mfg_state)
      action = np.random.choice(
          list(action_prob.keys()), p=list(action_prob.values())
      )
      mfg_state.apply_action(action)

  return total_reward

