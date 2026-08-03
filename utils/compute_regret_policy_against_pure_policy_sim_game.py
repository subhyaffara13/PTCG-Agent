import time

def compute_regret_policy_against_pure_policy_sim_game(game,
                                                       policy,
                                                       compute_true_value=False,
                                                       num_sample=100):
  time_tick = time.time()
  if compute_true_value:
    expected_value_policy = expected_game_score.policy_value(
        game.new_initial_state(), policy)[0]
  else:
    expected_value_policy = get_expected_value_sim_game(game, policy,
                                                        num_sample)
  worse_regret = 0
  policies = [
      PathBCEResponse(game, policy, 0),
      PathBCDEResponse(game, policy, 0),
      PathBDEResponse(game, policy, 0)
  ]
  for deviation_policy in policies:
    if compute_true_value:
      expected_value_noise = expected_game_score.policy_value(
          game.new_initial_state(), deviation_policy)[0]
    else:
      expected_value_noise = get_expected_value_sim_game(
          game, deviation_policy, num_sample, player=0)
    approximate_regret = expected_value_noise - expected_value_policy
    worse_regret = max(worse_regret, approximate_regret)
  return worse_regret, time.time() - time_tick

