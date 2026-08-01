
def mip_nash(game, objective, solver=None):
  """Solves for the optimal Nash for two-player general-sum games.

    Using mixed-integer programming:
      min f(x_0, x_1, p_mat)
      s.t.
      (u_0, u_1 are Nash payoffs variables of player 0 and 1)
      p_mat[0] * x_1 <= u_0
      x_0^T*p_mat[1] <= u_1
      (if a pure strategy is in the support then its payoff is Nash payoff)
      u_0 - p_mat[0] * x_1 <= u_max_0 * b_0
      u_1 - x_0^T*p_mat[1] <= u_max_1 * b_1
      (if a pure strategy is not in the support its probability mass is 0)
      x_0 <= 1 - b_0
      x_1 <= 1 - b_1
      (probability constraints)
      x_0 >= 0
      1^T * x_0 = 1
      x_1 >= 0
      1^T * x_1 = 1
      for all n, b_0[n] in {0, 1},
      for all m, b_1[m] in {0, 1},
      u_max_0, u_max_1 are the maximum payoff differences of player 0 and 1.
    Note: this formulation is a basic one that may only work well
    for simple objective function or low-dimensional inputs.
    GLPK_MI solver only handles linear objective.
    To handle nonlinear and high-dimensional cases,
    it is recommended to use advance solvers such as GUROBI,
    or use a piecewise linear approximation of the objective.
  Args:
    game: a pyspiel matrix game object
    objective: a string representing the objective (e.g., MAX_SOCIAL_WELFARE)
    solver: the mixed-integer solver used by cvxpy

  Returns:
    optimal Nash (x_0, x_1)
  """

  p_mat = game_payoffs_array(game)
  if len(p_mat) != 2:
    raise ValueError('MIP-Nash only works for two players.')

  assert len(p_mat) == 2
  assert p_mat[0].shape == p_mat[1].shape

  (m_0, m_1) = p_mat[0].shape

  u_max_0 = np.max(p_mat[0]) - np.min(p_mat[0])
  u_max_1 = np.max(p_mat[1]) - np.min(p_mat[1])

  x_0 = cp.Variable(m_0)
  x_1 = cp.Variable(m_1)
  u_0 = cp.Variable(1)
  u_1 = cp.Variable(1)
  b_0 = cp.Variable(m_0, boolean=True)
  b_1 = cp.Variable(m_1, boolean=True)

  u_m = p_mat[0] @ x_1
  u_n = x_0 @ p_mat[1]

  # probabilities constraints
  constraints = [x_0 >= 0, x_1 >= 0, cp.sum(x_0) == 1, cp.sum(x_1) == 1]
  # support constraints
  constraints.extend([u_m <= u_0, u_0 - u_m <= u_max_0 * b_0, x_0 <= 1 - b_0])
  constraints.extend([u_n <= u_1, u_1 - u_n <= u_max_1 * b_1, x_1 <= 1 - b_1])

  variables = {
      'x_0': x_0,
      'x_1': x_1,
      'u_0': u_0,
      'u_1': u_1,
      'b_0': b_0,
      'b_1': b_1,
      'p_mat': p_mat,
  }

  obj = TWO_PLAYER_OBJECTIVE[objective](variables)
  prob = cp.Problem(obj, constraints)
  prob.solve(solver=solver)

  return _simplex_projection(x_0.value.reshape(-1)), _simplex_projection(
      x_1.value.reshape(-1)
  )

