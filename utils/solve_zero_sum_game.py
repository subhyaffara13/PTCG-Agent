
def solve_zero_sum_game(game, solver=lp_solver.DEFAULT_SOLVER):
  """Solve the two-player zero-sum game using sequence-form LPs.

  Args:
    game: the spiel game tp solve (must be zero-sum, sequential, and have chance
      mode of deterministic or explicit stochastic).
    solver: a specific solver to use, sent to cvxpy (i.e. 'ecos', 'osqp ',
      'glpk'). A value of None uses cvxpy's default solver.

  Returns:
    A 4-tuple containing:
      - player 0 value
      - player 1 value
      - player 0 policy: a policy.TabularPolicy for player 0
      - player 1 policy: a policy.TabularPolicy for player 1
  """
  assert game.num_players() == 2
  assert game.get_type().utility == pyspiel.GameType.Utility.ZERO_SUM
  assert game.get_type().dynamics == pyspiel.GameType.Dynamics.SEQUENTIAL
  assert (
      game.get_type().chance_mode == pyspiel.GameType.ChanceMode.DETERMINISTIC
      or game.get_type().chance_mode
      == pyspiel.GameType.ChanceMode.EXPLICIT_STOCHASTIC
  )
  # There are several import matrices and vectors that form the LPs that
  # are built by this function:
  #
  # A is expected payoff to p1 of each (infoset0,action0) + (infoset1,action1)
  #   belong to p1 and p2 respectively, which lead to a terminal state. It has
  #   dimensions (infoset-actions0) x (infoset-actions1)
  # E,F are p1 / p2's strategy matrices (infosets) x (infoset-actions)
  # e,f are infosets+ x 1 column vector of (1 0 0 ... 0)
  # p,q are unconstrained variables each with infosets x 1.
  # x,y are realization plans of size infoset-actions
  #
  # In each of the computations above there is a special "root infoset" and
  # "root infoset-action" denote \emptyset. So the values are actually equal to
  # number of infosets + 1 and infoset-actions + 1.
  #
  # Equation (8) is   min_{y,p} e^T p
  #
  #             s.t.  -Ay + E^t p >= 0
  #                   -Fy          = -f
  #                     y         >= 0
  #
  # Equation (9) is   max_{x,q} -q^T f
  #
  #             s.t.  x^t(-A) - q^t F <= 0
  #                   x^t E^t          = e^t
  #                   x               >= 0
  #
  # So, the first LP has:
  #  - |y| + |p| variables (infoset-actions1 + infosets0)
  #  - infoset-actions0 inequality constraints (other than var lower-bounds)
  #  - infosets1 equality constraints
  #
  # And the second LP has:
  #  - |x| + |q| variables (infoset-actions0 + infosets1)
  #  - infoset-actions1 inequality constraints (other than var lower-bounds)
  #  - infosets0 equality constraints
  infosets = [{_EMPTY_INFOSET_KEYS[0]: 0}, {_EMPTY_INFOSET_KEYS[1]: 0}]
  infoset_actions = [
      {_EMPTY_INFOSET_ACTION_KEYS[0]: 0},
      {_EMPTY_INFOSET_ACTION_KEYS[1]: 0},
  ]
  infoset_action_maps = [{}, {}]
  depths = [0, 0]
  lps = [
      lp_solver.LinearProgram(lp_solver.ObjectiveType.OBJ_MIN),  # Eq. (8)
      lp_solver.LinearProgram(lp_solver.ObjectiveType.OBJ_MAX),  # Eq. (9)
  ]
  # Root-level variables and constraints.
  lps[0].add_or_reuse_variable(_EMPTY_INFOSET_ACTION_KEYS[1], lb=0)  # y root
  lps[0].add_or_reuse_variable(_EMPTY_INFOSET_KEYS[0])  # p root
  lps[1].add_or_reuse_variable(_EMPTY_INFOSET_ACTION_KEYS[0], lb=0)  # x root
  lps[1].add_or_reuse_variable(_EMPTY_INFOSET_KEYS[1])  # q root
  # objective coefficients
  lps[0].set_obj_coeff(_EMPTY_INFOSET_KEYS[0], 1.0)  # e^t p
  lps[1].set_obj_coeff(_EMPTY_INFOSET_KEYS[1], -1.0)  # -q^t f
  # y_root = 1  (-Fy = -f)
  lps[0].add_or_reuse_constraint(
      _EMPTY_INFOSET_KEYS[1], lp_solver.ConstraintType.CONS_TYPE_EQ
  )
  lps[0].set_cons_coeff(
      _EMPTY_INFOSET_KEYS[1], _EMPTY_INFOSET_ACTION_KEYS[1], -1.0
  )
  lps[0].set_cons_rhs(_EMPTY_INFOSET_KEYS[1], -1.0)
  # x_root = 1  (x^t E^t = e^t)
  lps[1].add_or_reuse_constraint(
      _EMPTY_INFOSET_KEYS[0], lp_solver.ConstraintType.CONS_TYPE_EQ
  )
  lps[1].set_cons_coeff(
      _EMPTY_INFOSET_KEYS[0], _EMPTY_INFOSET_ACTION_KEYS[0], 1.0
  )
  lps[1].set_cons_rhs(_EMPTY_INFOSET_KEYS[0], 1.0)
  _construct_lps(
      game.new_initial_state(),
      infosets,
      infoset_actions,
      infoset_action_maps,
      1.0,
      lps,
      _EMPTY_INFOSET_KEYS[:],
      _EMPTY_INFOSET_ACTION_KEYS[:],
      slack_variables=False,
      depths=depths,
      eps=0.0,
  )
  # Solve the programs.
  solutions = [lps[0].solve(solver=solver), lps[1].solve(solver=solver)]
  # Extract the policies (convert from realization plan to behavioral form).
  policies = [policy.TabularPolicy(game), policy.TabularPolicy(game)]
  _realisation_plans_to_policies(policies, lps, solutions, infoset_action_maps)

  return (
      solutions[0][lps[0].get_var_id(_EMPTY_INFOSET_KEYS[0])],
      solutions[1][lps[1].get_var_id(_EMPTY_INFOSET_KEYS[1])],
      policies[0],
      policies[1],
  )

