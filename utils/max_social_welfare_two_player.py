
def max_social_welfare_two_player(variables):
  """Max social welfare objective."""
  return cp.Maximize(variables['u_0'] + variables['u_1'])

