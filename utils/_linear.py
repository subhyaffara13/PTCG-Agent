
def _linear(
    payoff,
    a_mat,
    e_vec,
    action_repeats=None,
    solver_kwargs=None,
    cost=None):
  """Returns linear solution.

  This is a linear program.

  Args:
    payoff: A [NUM_PLAYER, NUM_ACT_0, NUM_ACT_1, ...] shape payoff tensor.
    a_mat: Constaint matrix.
    e_vec: Epsilon vector.
    action_repeats: List of action repeat counts.
    solver_kwargs: Solver kwargs.
    cost: Cost function of same shape as payoff.

  Returns:
    An epsilon-correlated equilibrium.
  """
  num_players = payoff.shape[0]
  num_actions = payoff.shape[1:]
  num_dists = int(np.prod(num_actions))

  if solver_kwargs is None:
    solver_kwargs = DEFAULT_ECOS_SOLVER_KWARGS

  if a_mat.shape[0] > 0:
    # Variables.
    x = cp.Variable(num_dists, nonneg=True)

    # Classifier.
    epsilon_dists = cp.matmul(a_mat, x) - e_vec

    # Constraints.
    dist_eq_con = cp.sum(x) == 1
    cor_lb_con = epsilon_dists <= 0

    # Objective.
    if cost is None:
      player_totals = [
          cp.sum(cp.multiply(payoff[p].flat, x)) for p in range(num_players)]
      reward = cp.sum(player_totals)
    else:
      reward = cp.sum(cp.multiply(cost.flat, x))
    obj = cp.Maximize(reward)

    prob = cp.Problem(obj, [
        dist_eq_con,
        cor_lb_con,
    ])

    # Solve.
    prob.solve(**solver_kwargs)
    status = prob.status

    # Distribution.
    dist = np.reshape(x.value, num_actions)

    # Other.
    val = reward.value
  else:
    if action_repeats is not None:
      repeat_factor, _ = _get_repeat_factor(action_repeats)
      x = repeat_factor / np.sum(repeat_factor)
    else:
      x = np.ones([num_dists]) / num_dists
    val = 0.0  # Fix me.
    dist = np.reshape(x, num_actions)
    status = None

  meta = dict(
      x=x,
      a_mat=a_mat,
      val=val,
      status=status,
      payoff=payoff,
      consistent=True,
      unique=False,
  )

  return dist, meta

