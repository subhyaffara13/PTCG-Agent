
def update_regrets_plus(regret):
  """Clamps the regrets to be non-negative."""
  return regret * (regret > 0)

