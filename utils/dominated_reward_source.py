
def dominated_reward_source(last_action, distribution):
  nu_a, nu_b, nu_c, *_ = distribution
  if last_action == 0:
    return nu_a + nu_c
  elif last_action == 1:
    return nu_b
  elif last_action == 2:
    return nu_a + nu_c - 0.25
  else:
    raise ValueError("Unknown last action " + str(last_action))

