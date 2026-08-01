
def compute_regret_policy(game,
                          policy,
                          num_random_policy_tested=10,
                          num_sample=100):
  time_tick = time.time()
  expected_value_policy = get_expected_value(game, policy, num_sample)
  worse_regret = 0
  for _ in range(num_random_policy_tested):
    noisy_n_policy = noisy_policy.NoisyPolicy(policy, player_id=0, alpha=1)
    expected_value_noise = get_expected_value(
        game, noisy_n_policy, num_sample, player=0)
    approximate_regret = expected_value_noise - expected_value_policy
    worse_regret = max(worse_regret, approximate_regret)
  return worse_regret, time.time() - time_tick

