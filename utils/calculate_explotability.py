
def calculate_explotability(game, distrib, policy):
  """This function is used to log the results to tensor board."""
  initial_states = game.new_initial_states()
  pi_value = policy_value.PolicyValue(
      game, distrib, policy, value.TabularValueFunction(game)
  )
  m = {
      f"ppo_br/{state}": pi_value.eval_state(state) for state in initial_states
  }
  nashc = NashC(game, distrib, pi_value).nash_conv()
  m["nash_conv_ppo"] = nashc

  return m

