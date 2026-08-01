
def cluster_strats(pi, matching_decimals=4):
  """Clusters strategies using stationary distribution (pi) masses.

  Args:
    pi: stationary distribution.
    matching_decimals: the number of stationary distribution decimals that
      should match for strategies to be considered in the same cluster.

  Returns:
    Dictionary that maps unique stationary distribution masses to strategies.
  """

  rounded_masses = pi.round(decimals=matching_decimals)
  masses_to_strats = {}
  for i in np.unique(rounded_masses):
    masses_to_strats[i] = np.where(rounded_masses == i)[0]
  return masses_to_strats

