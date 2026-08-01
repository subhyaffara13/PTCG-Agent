
def min_social_welfare_two_player(variables):
  """Min social welfare objective."""
  return cp.Minimize(variables['u_0'] + variables['u_1'])

