
def cce_gap(game, policies, weights, mus, nus, rewards=None,
            compute_true_rewards=False):
  if compute_true_rewards:
    rewards = compute_rewards(game, policies, mus)
  assert rewards is not None, ("Must provide rewards matrix when computing CCE "
                               "Gap.")
  _, gap = cce_br(game, policies, weights, mus, nus, rewards=rewards)
  return gap

