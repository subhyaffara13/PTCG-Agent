
def mean_field_uniform_policy(mfg_game,
                              number_of_iterations,
                              compute_metrics=False):
  del number_of_iterations
  uniform_policy = policy_module.UniformRandomPolicy(mfg_game)
  if compute_metrics:
    distribution_mfg = distribution_module.DistributionPolicy(
        mfg_game, uniform_policy)
    policy_value_ = policy_value.PolicyValue(mfg_game, distribution_mfg,
                                             uniform_policy).value(
                                                 mfg_game.new_initial_state())
    return uniform_policy, policy_value_
  return uniform_policy

