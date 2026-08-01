
def coop_reward(last_action, distribution):
  """A game incentivising cooperation."""
  nu_a, nu_b, nu_c, *_ = distribution
  if last_action == 0:
    return 10 * nu_a - 200 / 9 * (nu_a - nu_c) * nu_c - 20 * nu_b
  elif last_action == 1:
    return 20 * (nu_a - nu_b) - 2380 * nu_c
  elif last_action == 2:
    return 2000 / 9 * (nu_a - nu_c) * nu_c
  else:
    raise ValueError("Unknown last action " + str(last_action))

