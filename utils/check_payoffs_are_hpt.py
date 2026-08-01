
def check_payoffs_are_hpt(payoff_tables):
  """Returns True if payoffs are in HPT format."""
  if isinstance(payoff_tables[0], np.ndarray):
    return False
  elif hasattr(payoff_tables[0], "is_hpt") and payoff_tables[0].is_hpt:
    return True
  else:
    raise TypeError("payoff_tables should be a list of payoff matrices/hpts.")

