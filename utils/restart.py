
def restart(dummy_obs, num_players):
  all_obs = {
      "info_state": [dummy_obs.copy() for i in range(num_players)],
      "legal_actions": [np.zeros(3)],
      "prediction_label": 0,
  }
  return rl_environment.TimeStep(
      all_obs, [0.0], None, rl_environment.StepType.FIRST
  )

