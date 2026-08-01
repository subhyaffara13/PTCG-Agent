
def get_label_from_strat_profile(num_populations, strat_profile, strat_labels):
  """Returns a human-readable label corresponding to the strategy profile.

  E.g., for Rock-Paper-Scissors, strategies 0,1,2 have labels "R","P","S".
  For strat_profile (1,2,0,1), this returns "(P,S,R,P)". If strat_profile is a
  single strategy (e.g., 0) this returns just its label (e.g., "R").

  Args:
    num_populations: Number of populations.
    strat_profile: Strategy profile of interest.
    strat_labels: Strategy labels.

  Returns:
    Human-readable label string.
  """
  if num_populations == 1:
    return strat_labels[strat_profile]
  else:
    label = "("
    for i_population, i_strat in enumerate(strat_profile):
      label += strat_labels[i_population][i_strat]
      if i_population < len(strat_profile) - 1:
        label += ","
    label += ")"
    return label

