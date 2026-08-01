
def biased_indirect_rps(last_action, distribution):
  """Biased indirect Rock Paper Scissors."""
  nu_a = 0.7 * distribution[0]
  nu_b = 0.5 * distribution[1]
  nu_c = 0.3 * distribution[2]
  if last_action == 0:
    return nu_b - nu_c
  elif last_action == 1:
    return nu_c - nu_a
  elif last_action == 2:
    return nu_a - nu_b
  else:
    raise ValueError("Unknown last action " + str(last_action))

