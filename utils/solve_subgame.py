
def solve_subgame(subgame_payoffs):
  """Solves the subgame using OpenSpiel's LP solver."""
  p0_sol, p1_sol, _, _ = lp_solver.solve_zero_sum_matrix_game(
      pyspiel.create_matrix_game(*subgame_payoffs))
  p0_sol, p1_sol = np.asarray(p0_sol), np.asarray(p1_sol)
  return [p0_sol / p0_sol.sum(), p1_sol / p1_sol.sum()]

