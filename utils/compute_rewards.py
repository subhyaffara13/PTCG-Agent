
def compute_rewards(game, policies, mus):
  return np.array([
      [utils.get_exact_value(pi, mu, game) for pi in policies] for mu in mus
  ])

