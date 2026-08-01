
def solve_perturbed_zero_sum_game(
    game,
    solver=lp_solver.DEFAULT_SOLVER,
    eps: float = 0.0,
):
  """Solve the two-player zero-sum game using sequence-form LPs.

    This function computes a sequential equilibrium based on
    perturbed LPs from [2].

  Args:
    game: the spiel game tp solve (must be zero-sum, sequential, and have chance
      mode of deterministic or explicit stochastic).
    solver: a specific solver to use, sent to cvxpy (i.e. 'ecos', 'osqp',
      'glpk'). A value of None uses cvxpy's default solver.
    eps: eps: perturbation strength ( 0.0 = classic KMvS Nash, 1e-8 = sequential
      eq.)

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
  # u,v are slack variables of size infoset-actions
  #
  # In each of the computations above there is a special "root infoset" and
  # "root infoset-action" denote \emptyset. So the values are actually equal to
  # number of infosets + 1 and infoset-actions + 1.
  #
  # Equation (2.4) is   min_{p,u,y} e^T p - (k_eps)^T u
  #
  #             s.t.  -Ay + E^T p - u >= 0
  #                   -Fy             = -f
  #                     y             >= l_eps
  #                                 u >= 0
  #
  # Equation (2.5) is   max_{q,v,x} q^T f + v^T (l_eps)
  #
  #             s.t.  -x^T(-A) + q^T F + v  <= 0
  #                   x^T E^T               = e^T
  #                   x                     >= k_eps
  #                                      v  >= 0
  #
  # So, the first LP has:
  #  - |y| + |p| (+ |u|) variables (infoset-actions1 + infosets0 + slacks0)
  #  - infoset-actions0 inequality constraints (other than var lower-bounds)
  #  - infosets1 equality constraints
  #
  # And the second LP has:
  #  - |x| + |q| (+ |v|) variables (infoset-actions0 + infosets1 + slacks1)
  #  - infoset-actions1 inequality constraints (other than var lower-bounds)
  #  - infosets0 equality constraints
  #
  # NOTE: the slacks can be handled by the solver.
  #
  infosets = [{_EMPTY_INFOSET_KEYS[0]: 0}, {_EMPTY_INFOSET_KEYS[1]: 0}]
  infoset_actions = [
      {_EMPTY_INFOSET_ACTION_KEYS[0]: 0},
      {_EMPTY_INFOSET_ACTION_KEYS[1]: 0},
  ]
  infoset_action_maps = [{}, {}]
  depths = [0, 0]

  lps = [
      lp_solver.LinearProgram(lp_solver.ObjectiveType.OBJ_MIN),  # Eq. (2.4)
      lp_solver.LinearProgram(lp_solver.ObjectiveType.OBJ_MAX),  # Eq. (2.5)
  ]

  root_eps = eps if eps > 0 else 0

  lps[0].add_or_reuse_variable(_EMPTY_INFOSET_ACTION_KEYS[1], lb=0.0)  # y_root
  lps[0].add_or_reuse_variable(_EMPTY_INFOSET_KEYS[0])  # p_root

  u_root = "u_" + _EMPTY_INFOSET_ACTION_KEYS[0]
  lps[0].add_or_reuse_variable(u_root, lb=0.0)
  lps[0].add_or_reuse_constraint(
      _EMPTY_INFOSET_ACTION_KEYS[0], lp_solver.ConstraintType.CONS_TYPE_GEQ
  )
  # - (k_eps)^T u_root
  lps[0].set_cons_coeff(_EMPTY_INFOSET_ACTION_KEYS[0], u_root, -1.0)
  lps[0].set_obj_coeff(u_root, -root_eps)

  lps[1].add_or_reuse_variable(_EMPTY_INFOSET_ACTION_KEYS[0], lb=0.0)  # x_root
  lps[1].add_or_reuse_variable(_EMPTY_INFOSET_KEYS[1])  # q_root

  v_root = "v_" + _EMPTY_INFOSET_ACTION_KEYS[1]
  lps[1].add_or_reuse_variable(v_root, lb=0.0)
  lps[1].add_or_reuse_constraint(
      _EMPTY_INFOSET_ACTION_KEYS[1], lp_solver.ConstraintType.CONS_TYPE_LEQ
  )
  # + v^T (l_eps)
  lps[1].set_cons_coeff(_EMPTY_INFOSET_ACTION_KEYS[1], v_root, 1.0)
  lps[1].set_obj_coeff(v_root, root_eps)

  # objective coefficients
  lps[0].set_obj_coeff(_EMPTY_INFOSET_KEYS[0], 1.0)
  lps[1].set_obj_coeff(_EMPTY_INFOSET_KEYS[1], -1.0)

  # y_root = 1  (-Fy = -f), same eq. constraints
  lps[0].add_or_reuse_constraint(
      _EMPTY_INFOSET_KEYS[1], lp_solver.ConstraintType.CONS_TYPE_EQ
  )
  lps[0].set_cons_coeff(
      _EMPTY_INFOSET_KEYS[1], _EMPTY_INFOSET_ACTION_KEYS[1], -1.0
  )
  lps[0].set_cons_rhs(_EMPTY_INFOSET_KEYS[1], -1.0)

  # x_root = 1  (x^T E^T = e^T), same eq. constraints
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
      slack_variables=True,
      depths=depths,
      eps=eps if eps > 0.0 else 0.0,
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

