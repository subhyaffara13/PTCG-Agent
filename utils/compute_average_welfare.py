
def compute_average_welfare(game, policies, mus, rhos, nus):
  """Computes average welfare.

  Args:
    game: Pyspiel game.
    policies: List of policies, length P
    mus: List of State Distributions of length T
    rhos: Temporal weights, length T
    nus: Policy distribution per time, shape [T, P]

  Returns:
    Average welfare.
  """
  assert len(mus) == len(rhos)
  assert len(rhos) == nus.shape[0]
  assert len(policies) == nus.shape[1]

  rewards = compute_rewards(game, policies, mus)
  return np.sum(rewards * nus * rhos.reshape(-1, 1))

