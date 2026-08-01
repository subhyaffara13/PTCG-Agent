
def compute_payoff(row_profile, col_profile, row_payoff_table):
  """Returns row's expected payoff in a bimatrix game.

  Args:
    row_profile: Row's strategy profile.
    col_profile: Column's strategy profile.
    row_payoff_table: Row's payoff table.
  """

  return np.dot(np.dot(row_profile.T, row_payoff_table), col_profile)

