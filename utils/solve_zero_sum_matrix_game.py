
def solve_zero_sum_matrix_game(game):
  """Solves a matrix game by using linear programming.

  Args:
    game: a pyspiel MatrixGame

  Returns:
    A 4-tuple containing:
      - p0_sol (array-like): probability distribution over row actions
      - p1_sol (array-like): probability distribution over column actions
      - p0_sol_value, expected value to the first player
      - p1_sol_value, expected value to the second player
  """

  # Solving a game for player i (e.g. row player) requires finding a mixed
  # policy over player i's pure strategies (actions) such that a value of the
  # mixed strategy against every opponent pure strategy is maximized.
  #
  # For more detail, please refer to Sec 4.1 of Shoham & Leyton-Brown, 2009:
  # Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations
  # http://www.masfoundations.org/mas.pdf
  #
  # For the row player the LP looks like:
  #    max V
  #     st. sigma_a1 \dot col_0 >= V
  #         sigma_a2 \dot col_1 >= V
  #              .
  #              .
  #         sigma_am \cot col_n >= V
  #         for all i, sigma_ai >= 0
  #         sigma \dot 1 = 1
  assert isinstance(game, pyspiel.MatrixGame)
  assert game.get_type().information == pyspiel.GameType.Information.ONE_SHOT
  assert game.get_type().utility == pyspiel.GameType.Utility.ZERO_SUM
  num_rows = game.num_rows()
  num_cols = game.num_cols()

  # First, do the row player (player 0).
  lp0 = LinearProgram(ObjectiveType.OBJ_MAX)
  for r in range(num_rows):  # one var per action / pure strategy
    lp0.add_or_reuse_variable(r, lb=0)
  lp0.add_or_reuse_variable(num_rows)  # V
  lp0.set_obj_coeff(num_rows, 1.0)  # max V
  for c in range(num_cols):
    lp0.add_or_reuse_constraint(c, ConstraintType.CONS_TYPE_GEQ)
    for r in range(num_rows):
      lp0.set_cons_coeff(c, r, game.player_utility(0, r, c))
    lp0.set_cons_coeff(c, num_rows, -1.0)  # -V >= 0
  lp0.add_or_reuse_constraint(num_cols + 1, ConstraintType.CONS_TYPE_EQ)
  lp0.set_cons_rhs(num_cols + 1, 1.0)
  for r in range(num_rows):
    lp0.set_cons_coeff(num_cols + 1, r, 1.0)
  sol = lp0.solve()
  p0_sol = sol[:-1]
  p0_sol_val = sol[-1]

  # Now, the column player (player 1).
  lp1 = LinearProgram(ObjectiveType.OBJ_MAX)
  for c in range(num_cols):  # one var per action / pure strategy
    lp1.add_or_reuse_variable(c, lb=0)
  lp1.add_or_reuse_variable(num_cols)  # V
  lp1.set_obj_coeff(num_cols, 1)  # max V
  for r in range(num_rows):
    lp1.add_or_reuse_constraint(r, ConstraintType.CONS_TYPE_GEQ)
    for c in range(num_cols):
      lp1.set_cons_coeff(r, c, game.player_utility(1, r, c))
    lp1.set_cons_coeff(r, num_cols, -1.0)  # -V >= 0
  lp1.add_or_reuse_constraint(num_rows + 1, ConstraintType.CONS_TYPE_EQ)
  lp1.set_cons_rhs(num_rows + 1, 1.0)
  for c in range(num_cols):
    lp1.set_cons_coeff(num_rows + 1, c, 1.0)
  sol = lp1.solve()
  p1_sol = sol[:-1]
  p1_sol_val = sol[-1]

  return p0_sol, p1_sol, p0_sol_val, p1_sol_val

