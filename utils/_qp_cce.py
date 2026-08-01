
def _qp_cce(
    payoff,
    a_mats,
    e_vecs,
    assume_full_support=False,
    action_repeats=None,
    solver_kwargs=None,
    min_epsilon=False):
  """Returns the correlated equilibrium with maximum Gini impurity.

  Args:
    payoff: A [NUM_PLAYER, NUM_ACT_0, NUM_ACT_1, ...] shape payoff tensor.
    a_mats: A [NUM_CON, PROD(A)] shape gain tensor.
    e_vecs: Epsilon vector.
    assume_full_support: Whether to ignore beta values.
    action_repeats: Vector of action repeats for each player.
    solver_kwargs: Additional kwargs for solver.
    min_epsilon: Whether to minimize epsilon.

  Returns:
    An epsilon-correlated equilibrium.
  """
  num_players = payoff.shape[0]
  num_actions = payoff.shape[1:]
  num_dists = int(np.prod(num_actions))

  if solver_kwargs is None:
    solver_kwargs = DEFAULT_OSQP_SOLVER_KWARGS

  epsilon = None
  nonzero_cons = [a_mat.shape[0] > 0 for a_mat in a_mats if a_mat is not None]
  if any(nonzero_cons):
    x = cp.Variable(num_dists, nonneg=(not assume_full_support))
    if min_epsilon:
      epsilon = cp.Variable(nonpos=True)
      e_vecs = [epsilon] * num_players

    if action_repeats is not None:
      repeat_factor, _ = _get_repeat_factor(action_repeats)
      x_repeated = cp.multiply(x, repeat_factor)
      dist_eq_con = cp.sum(x_repeated) == 1
      cor_lb_cons = [
          cp.matmul(a_mat, cp.multiply(x, repeat_factor)) <= e_vec
          for a_mat, e_vec in
          zip(a_mats, e_vecs) if a_mat.size > 0]
      eye = sp.sparse.diags(repeat_factor)
    else:
      repeat_factor = 1
      x_repeated = x
      dist_eq_con = cp.sum(x_repeated) == 1
      cor_lb_cons = [
          cp.matmul(a_mat, x) <= e_vec for a_mat, e_vec in
          zip(a_mats, e_vecs) if a_mat.size > 0]
      eye = sp.sparse.eye(num_dists)

    # This is more memory efficient than using cp.sum_squares.
    cost = 1 - cp.quad_form(x, eye)
    if min_epsilon:
      cost -= cp.multiply(2, epsilon)

    obj = cp.Maximize(cost)
    prob = cp.Problem(obj, [dist_eq_con] + cor_lb_cons)
    cost_value = prob.solve(**solver_kwargs)
    status = prob.status
    alphas = [cor_lb_con.dual_value for cor_lb_con in cor_lb_cons]
    lamb = dist_eq_con.dual_value

    val = cost.value
    x = x_repeated.value
    dist = np.reshape(x, num_actions)
  else:
    cost_value = 0.0
    val = 1 - 1 / num_dists
    if action_repeats is not None:
      repeat_factor, _ = _get_repeat_factor(action_repeats)
      x = repeat_factor / np.sum(repeat_factor)
    else:
      x = np.ones([num_dists]) / num_dists
    dist = np.reshape(x, num_actions)
    status = None
    alphas = [np.zeros([])]
    lamb = None

  meta = dict(
      x=x,
      a_mats=a_mats,
      status=status,
      cost=cost_value,
      val=val,
      alphas=alphas,
      lamb=lamb,
      unique=True,
      min_epsilon=None if epsilon is None else epsilon.value,
  )
  return dist, meta

