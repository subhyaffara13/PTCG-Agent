
def get_nu_values(policies, nu, game):
  rewards = np.zeros(len(policies))
  mu = distribution.DistributionPolicy(
      game, MergedPolicy(game, None, policies, nu)
  )
  for index, policy in enumerate(policies):
    rewards[index] = sample_value(policy, mu, game)
  return rewards

